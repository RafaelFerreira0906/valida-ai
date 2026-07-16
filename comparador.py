import os  
import re  
from copy import deepcopy  
from decimal import Decimal, InvalidOperation  
from datetime import datetime  
  
from reportlab.lib import colors  
from reportlab.lib.pagesizes import A4, landscape  
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  
from reportlab.lib.units import mm  
from reportlab.platypus import (  
    SimpleDocTemplate,  
    Paragraph,  
    Spacer,  
    Table,  
    TableStyle,  
    PageBreak  
)  
  
ALLOWED_EXTENSIONS = (".json",)  
  
MAPEAMENTO_TIPOS = {  
    "e_analise_granulometrica": ("Análise Granulométrica", "analise_granulometrica"),  
    "e_certidao_inteiro_teor": ("Certidão de Inteiro Teor", "certidao_inteiro_teor"),  
    "e_contrato_de_locacao": ("Contrato de Locação", "contrato_de_locacao"),  
    "e_contrato_social": ("Contrato Social", "contrato_social"),  
    "e_declaracao_posse_terceiros": ("Declaração de Posse", "declaracao_posse"),  
    "e_demonstracoes_contabeis": ("Demonstrações Contábeis", "demonstracoes_contabeis"),  
    "e_fianca_bancaria": ("Fiança Bancária", "fianca_bancaria"),  
    "e_aditivo_fianca_bancaria": ("Aditivo de Fiança Bancária", "aditivo_fianca_bancaria"),  
    "e_orcamento_fne_sol": ("Orçamento FNE SOL", "orcamento_fne_sol"),  
    "e_parecer_gerencial": ("Parecer Gerencial", "parecer_gerencial"),  
    "e_procuracao": ("Procuração", "procuracao"),  
    "e_titulo_dominio": ("Título de Domínio", "titulo_dominio"),  
}  
  
OPTIONAL_EXACT_PATHS = {  
    "complemento",  
    "observacao",  
    "observacoes",  
    "obs",  
    "email_secundario",  
    "telefone_secundario",  
    "referencia",  
    "descricao_complementar",  
}  
  
OPTIONAL_KEYWORDS = {  
    "complemento",  
    "observacao",  
    "observacoes",  
    "obs",  
    "referencia",  
    "anexo",  
    "email_secundario",  
    "telefone_secundario",  
}  
  
HEAVY_WEIGHT_KEYWORDS = {  
    "cpf": 10,  
    "cnpj": 10,  
    "razao_social": 9,  
    "nome_empresarial": 9,  
    "nome": 7,  
    "data": 7,  
    "data_abertura": 8,  
    "data_emissao": 8,  
    "matricula": 8,  
    "numero": 6,  
    "valor": 8,  
    "capital_social": 9,  
    "vigencia": 8,  
    "tipo_documento": 8,  
    "ged": 10,  
}  
  
LOW_WEIGHT_KEYWORDS = {  
    "bairro": 3,  
    "complemento": 2,  
    "referencia": 2,  
    "uf": 4,  
    "logradouro": 5,  
    "endereco": 5,  
    "cep": 5,  
}  
  
LIST_MATCH_KEYS = [  
    "id",  
    "codigo",  
    "cpf",  
    "cnpj",  
    "numero",  
    "matricula",  
    "nome",  
    "descricao",  
]  
  
  
def detectar_tipo_documental(json_data):  
    if not isinstance(json_data, dict):  
        raise ValueError("O JSON enviado precisa ser um objeto na raiz.")  
    if not json_data:  
        raise ValueError("O JSON enviado está vazio.")  
  
    primeira_chave = next(iter(json_data.keys()))  
  
    if primeira_chave not in MAPEAMENTO_TIPOS:  
        raise ValueError(f"Tipo documental não mapeado: '{primeira_chave}'.")  
  
    nome_legivel, pasta_gabarito = MAPEAMENTO_TIPOS[primeira_chave]  
    return primeira_chave, nome_legivel, pasta_gabarito  
  
  
def obter_ged_do_arquivo(nome_arquivo):  
    base, ext = os.path.splitext(nome_arquivo)  
    if ext.lower() != ".json":  
        raise ValueError("O arquivo enviado deve ter extensão .json.")  
    ged = base.strip()  
    if not ged:  
        raise ValueError("Não foi possível identificar o GED pelo nome do arquivo.")  
    return ged  
  
  
def localizar_gabarito(base_gabaritos, pasta_gabarito, ged):  
    caminho = os.path.join(base_gabaritos, pasta_gabarito, f"{ged}.json")  
    if not os.path.exists(caminho):  
        raise FileNotFoundError(  
            f"Gabarito não encontrado para o GED '{ged}' em '{caminho}'."  
        )  
    return caminho  
  
  
def nome_tipo(valor):  
    if valor is None:  
        return "null"  
    if isinstance(valor, bool):  
        return "bool"  
    if isinstance(valor, int) and not isinstance(valor, bool):  
        return "int"  
    if isinstance(valor, float):  
        return "float"  
    if isinstance(valor, str):  
        return "str"  
    if isinstance(valor, dict):  
        return "dict"  
    if isinstance(valor, list):  
        return "list"  
    return type(valor).__name__  
  
  
def extrair_nome_campo(path):  
    if not path:  
        return ""  
    path = re.sub(r"$\d+$", "", path)  
    partes = path.split(".")  
    return partes[-1].lower() if partes else ""  
  
  
def path_has_keyword(path, keyword):  
    return keyword.lower() in path.lower()  
  
  
def eh_opcional(path):  
    campo = extrair_nome_campo(path)  
    if campo in OPTIONAL_EXACT_PATHS:  
        return True  
    path_lower = path.lower()  
    return any(k in path_lower for k in OPTIONAL_KEYWORDS)  
  
  
def peso_por_path(path):  
    path_lower = path.lower()  
    campo = extrair_nome_campo(path)  
  
    for chave, peso in HEAVY_WEIGHT_KEYWORDS.items():  
        if chave == campo or path_has_keyword(path_lower, chave):  
            return peso  
  
    for chave, peso in LOW_WEIGHT_KEYWORDS.items():  
        if chave == campo or path_has_keyword(path_lower, chave):  
            return peso  
  
    return 5  
  
  
def normalizar_texto(valor):  
    return re.sub(r"\s+", " ", valor.strip())  
  
  
def somente_digitos(valor):  
    return re.sub(r"\D", "", valor or "")  
  
  
def normalizar_cpf_cnpj(valor):  
    if valor is None:  
        return None  
    s = somente_digitos(str(valor))  
    if len(s) in (11, 14):  
        return s  
    return normalizar_texto(str(valor))  
  
  
def parse_decimal_brasil(valor):  
    if valor is None:  
        return None  
    if isinstance(valor, (int, float, Decimal)) and not isinstance(valor, bool):  
        return Decimal(str(valor))  
  
    s = str(valor).strip()  
    if not s:  
        return None  
  
    s = s.replace("R$", "").replace(" ", "")  
  
    if "." in s and "," in s:  
        s = s.replace(".", "").replace(",", ".")  
    elif "," in s:  
        s = s.replace(".", "").replace(",", ".")  
  
    try:  
        return Decimal(s)  
    except InvalidOperation:  
        return None  
  
  
def normalizar_data(valor):  
    if valor is None:  
        return None  
  
    if isinstance(valor, datetime):  
        return valor.strftime("%Y-%m-%d")  
  
    s = str(valor).strip()  
    if not s:  
        return ""  
  
    formatos = [  
        "%d/%m/%Y",  
        "%Y-%m-%d",  
        "%d-%m-%Y",  
        "%Y/%m/%d",  
        "%d/%m/%Y %H:%M:%S",  
        "%Y-%m-%d %H:%M:%S",  
        "%d-%m-%Y %H:%M:%S",  
    ]  
  
    for fmt in formatos:  
        try:  
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")  
        except ValueError:  
            continue  
  
    return normalizar_texto(s)  
  
  
def detectar_normalizador(path, valor):  
    path_lower = path.lower()  
    campo = extrair_nome_campo(path)  
  
    if "cpf" in campo or "cnpj" in campo or "cpf" in path_lower or "cnpj" in path_lower:  
        return "cpf_cnpj"  
  
    if "data" in campo or "data_" in campo or "dt_" in campo or ".data" in path_lower:  
        return "data"  
  
    if any(k in campo for k in ["valor", "montante", "capital", "preco", "preço", "total"]):  
        return "decimal"  
  
    if isinstance(valor, str):  
        if re.match(r"^\s*R?\$?\s?[\d\.\,]+\s*$", valor):  
            if any(k in path_lower for k in ["valor", "montante", "capital", "preco", "preço", "total"]):  
                return "decimal"  
  
    return "texto_ou_padrao"  
  
  
def normalizar_valor_por_regra(path, valor):  
    if valor is None:  
        return None  
  
    normalizador = detectar_normalizador(path, valor)  
  
    if normalizador == "cpf_cnpj":  
        return normalizar_cpf_cnpj(valor)  
    if normalizador == "data":  
        return normalizar_data(valor)  
    if normalizador == "decimal":  
        parsed = parse_decimal_brasil(valor)  
        return str(parsed) if parsed is not None else normalizar_texto(str(valor))  
    if isinstance(valor, str):  
        return normalizar_texto(valor)  
    return valor  
  
  
def valores_equivalentes(path, esperado, recebido):  
    normalizado_esperado = normalizar_valor_por_regra(path, esperado)  
    normalizado_recebido = normalizar_valor_por_regra(path, recebido)  
  
    if isinstance(normalizado_esperado, str) and isinstance(normalizado_recebido, str):  
        try:  
            dec_esp = Decimal(normalizado_esperado)  
            dec_rec = Decimal(normalizado_recebido)  
            if abs(dec_esp - dec_rec) <= Decimal("0.01"):  
                return True  
        except Exception:  
            pass  
  
    return normalizado_esperado == normalizado_recebido  
  
  
def contar_folhas_ponderadas(data, path=""):  
    if isinstance(data, dict):  
        if not data:  
            return peso_por_path(path or "$")  
        return sum(contar_folhas_ponderadas(v, f"{path}.{k}" if path else k) for k, v in data.items())  
  
    if isinstance(data, list):  
        if not data:  
            return peso_por_path(path or "$")  
        return sum(contar_folhas_ponderadas(item, f"{path}[{i}]") for i, item in enumerate(data))  
  
    return peso_por_path(path or "$")  
  
  
def severidade_por_item(tipo, path, peso):  
    if tipo in ("faltando_no_recebido", "tipo_diferente", "item_faltando_no_recebido"):  
        return "alta"  
    if peso >= 8:  
        return "alta"  
    if peso >= 5:  
        return "media"  
    return "baixa"  
  
  
def gerar_sugestao(item):  
    tipo = item.get("tipo")  
    path = item.get("path", "")  
    recebido = item.get("recebido")  
    esperado = item.get("esperado")  
  
    if tipo == "faltando_no_recebido":  
        return f"Incluir o campo '{path}' com valor compatível ao gabarito."  
    if tipo == "campo_extra_no_recebido":  
        return f"Remover o campo extra '{path}' ou cadastrá-lo como permitido."  
    if tipo == "item_faltando_no_recebido":  
        return f"Incluir o item ausente da lista em '{path}'."  
    if tipo == "item_extra_no_recebido":  
        return f"Remover o item excedente da lista em '{path}'."  
    if tipo == "tipo_diferente":  
        return f"Converter o tipo do campo '{path}' de '{recebido}' para '{esperado}'."  
    if tipo == "valor_diferente":  
        return f"Corrigir o valor do campo '{path}' para o padrão esperado."  
    return f"Revisar a regra de validação do campo '{path}'."  
  
  
def identificar_melhoria(item):  
    tipo = item.get("tipo")  
    path = item.get("path", "")  
  
    if tipo in ("faltando_no_recebido", "item_faltando_no_recebido"):  
        return f"Adicionar validação obrigatória e checklist pré-envio para '{path}'."  
    if tipo in ("campo_extra_no_recebido", "item_extra_no_recebido"):  
        return f"Aplicar saneamento de payload e whitelist de campos para '{path}'."  
    if tipo == "tipo_diferente":  
        return f"Implementar schema validation com coerção automática de tipo em '{path}'."  
    if tipo == "valor_diferente":  
        return f"Fortalecer normalização e regras de extração do campo '{path}'."  
    return f"Revisar a lógica de validação relacionada a '{path}'."  
  
  
def escolher_chave_match_lista(lista_esperada, lista_recebida):  
    listas = []  
    if isinstance(lista_esperada, list):  
        listas.extend(lista_esperada)  
    if isinstance(lista_recebida, list):  
        listas.extend(lista_recebida)  
  
    dicts = [x for x in listas if isinstance(x, dict)]  
    if not dicts:  
        return None  
  
    for candidate in LIST_MATCH_KEYS:  
        if all(candidate in d for d in dicts):  
            return candidate  
    return None  
  
  
def assinatura_item(item, chave_match):  
    if not isinstance(item, dict):  
        return None  
    if chave_match and chave_match in item:  
        return f"{chave_match}:{normalizar_valor_por_regra(chave_match, item.get(chave_match))}"  
    for k in LIST_MATCH_KEYS:  
        if k in item:  
            return f"{k}:{normalizar_valor_por_regra(k, item.get(k))}"  
    return None  
  
  
def registrar_diferenca(diferencas, path, tipo, esperado, recebido, peso):  
    diferencas.append({  
        "path": path or "$",  
        "tipo": tipo,  
        "esperado": esperado,  
        "recebido": recebido,  
        "peso": peso,  
        "severidade": severidade_por_item(tipo, path, peso),  
    })  
  
  
def comparar_jsons(esperado, recebido, path="", diferencas=None, estatisticas=None):  
    if diferencas is None:  
        diferencas = []  
  
    if estatisticas is None:  
        estatisticas = {  
            "campos_analisados": 0,  
            "campos_conformes": 0,  
            "campos_divergentes": 0,  
            "peso_total": Decimal("0"),  
            "peso_conforme": Decimal("0"),  
            "peso_divergente": Decimal("0"),  
            "penalidade_extras": Decimal("0")  
        }  
  
    if type(esperado) != type(recebido):  
        peso = Decimal(str(max(contar_folhas_ponderadas(esperado, path), 1)))  
        estatisticas["campos_analisados"] += 1  
        estatisticas["campos_divergentes"] += 1  
        estatisticas["peso_total"] += peso  
        estatisticas["peso_divergente"] += peso  
        registrar_diferenca(diferencas, path or "$", "tipo_diferente", nome_tipo(esperado), nome_tipo(recebido), float(peso))  
        return diferencas, estatisticas  
  
    if isinstance(esperado, dict):  
        chaves_esperadas = set(esperado.keys())  
        chaves_recebidas = set(recebido.keys())  
  
        faltando = sorted(chaves_esperadas - chaves_recebidas)  
        extras = sorted(chaves_recebidas - chaves_esperadas)  
        comuns = sorted(chaves_esperadas & chaves_recebidas)  
  
        for chave in faltando:  
            novo_path = f"{path}.{chave}" if path else chave  
            if eh_opcional(novo_path):  
                continue  
            peso = Decimal(str(contar_folhas_ponderadas(esperado[chave], novo_path)))  
            estatisticas["campos_analisados"] += 1  
            estatisticas["campos_divergentes"] += 1  
            estatisticas["peso_total"] += peso  
            estatisticas["peso_divergente"] += peso  
            registrar_diferenca(diferencas, novo_path, "faltando_no_recebido", esperado[chave], None, float(peso))  
  
        for chave in extras:  
            novo_path = f"{path}.{chave}" if path else chave  
            peso = Decimal(str(contar_folhas_ponderadas(recebido[chave], novo_path)))  
            estatisticas["campos_analisados"] += 1  
            estatisticas["campos_divergentes"] += 1  
            estatisticas["peso_total"] += peso  
            estatisticas["peso_divergente"] += peso  
            estatisticas["penalidade_extras"] += peso  
            registrar_diferenca(diferencas, novo_path, "campo_extra_no_recebido", None, recebido[chave], float(peso))  
  
        for chave in comuns:  
            novo_path = f"{path}.{chave}" if path else chave  
            comparar_jsons(esperado[chave], recebido[chave], novo_path, diferencas, estatisticas)  
  
        return diferencas, estatisticas  
  
    if isinstance(esperado, list):  
        chave_match = escolher_chave_match_lista(esperado, recebido)  
  
        if chave_match:  
            mapa_esperado = {}  
            mapa_recebido = {}  
            usados_fallback_esp = 0  
            usados_fallback_rec = 0  
  
            for item in esperado:  
                sig = assinatura_item(item, chave_match)  
                if sig is None:  
                    sig = f"__idx_esp__{usados_fallback_esp}"  
                    usados_fallback_esp += 1  
                mapa_esperado[sig] = item  
  
            for item in recebido:  
                sig = assinatura_item(item, chave_match)  
                if sig is None:  
                    sig = f"__idx_rec__{usados_fallback_rec}"  
                    usados_fallback_rec += 1  
                mapa_recebido[sig] = item  
  
            assinaturas = sorted(set(mapa_esperado.keys()) | set(mapa_recebido.keys()))  
  
            for sig in assinaturas:  
                item_esp = mapa_esperado.get(sig)  
                item_rec = mapa_recebido.get(sig)  
                novo_path = f"{path}[{sig}]"  
  
                if item_esp is None:  
                    peso = Decimal(str(contar_folhas_ponderadas(item_rec, novo_path)))  
                    estatisticas["campos_analisados"] += 1  
                    estatisticas["campos_divergentes"] += 1  
                    estatisticas["peso_total"] += peso  
                    estatisticas["peso_divergente"] += peso  
                    estatisticas["penalidade_extras"] += peso  
                    registrar_diferenca(diferencas, novo_path, "item_extra_no_recebido", None, item_rec, float(peso))  
                elif item_rec is None:  
                    peso = Decimal(str(contar_folhas_ponderadas(item_esp, novo_path)))  
                    estatisticas["campos_analisados"] += 1  
                    estatisticas["campos_divergentes"] += 1  
                    estatisticas["peso_total"] += peso  
                    estatisticas["peso_divergente"] += peso  
                    registrar_diferenca(diferencas, novo_path, "item_faltando_no_recebido", item_esp, None, float(peso))  
                else:  
                    comparar_jsons(item_esp, item_rec, novo_path, diferencas, estatisticas)  
  
            return diferencas, estatisticas  
  
        maior = max(len(esperado), len(recebido))  
        for i in range(maior):  
            novo_path = f"{path}[{i}]"  
            if i >= len(esperado):  
                peso = Decimal(str(contar_folhas_ponderadas(recebido[i], novo_path)))  
                estatisticas["campos_analisados"] += 1  
                estatisticas["campos_divergentes"] += 1  
                estatisticas["peso_total"] += peso  
                estatisticas["peso_divergente"] += peso  
                estatisticas["penalidade_extras"] += peso  
                registrar_diferenca(diferencas, novo_path, "item_extra_no_recebido", None, recebido[i], float(peso))  
            elif i >= len(recebido):  
                peso = Decimal(str(contar_folhas_ponderadas(esperado[i], novo_path)))  
                estatisticas["campos_analisados"] += 1  
                estatisticas["campos_divergentes"] += 1  
                estatisticas["peso_total"] += peso  
                estatisticas["peso_divergente"] += peso  
                registrar_diferenca(diferencas, novo_path, "item_faltando_no_recebido", esperado[i], None, float(peso))  
            else:  
                comparar_jsons(esperado[i], recebido[i], novo_path, diferencas, estatisticas)  
  
        return diferencas, estatisticas  
  
    peso = Decimal(str(peso_por_path(path or "$")))  
    estatisticas["campos_analisados"] += 1  
    estatisticas["peso_total"] += peso  
  
    if valores_equivalentes(path or "$", esperado, recebido):  
        estatisticas["campos_conformes"] += 1  
        estatisticas["peso_conforme"] += peso  
    else:  
        estatisticas["campos_divergentes"] += 1  
        estatisticas["peso_divergente"] += peso  
        registrar_diferenca(diferencas, path or "$", "valor_diferente", esperado, recebido, float(peso))  
  
    return diferencas, estatisticas  
  
  
def gerar_contadores(diferencas):  
    contadores = {  
        "valor_diferente": 0,  
        "faltando_no_recebido": 0,  
        "campo_extra_no_recebido": 0,  
        "tipo_diferente": 0,  
        "item_extra_no_recebido": 0,  
        "item_faltando_no_recebido": 0,  
        "alta": 0,  
        "media": 0,  
        "baixa": 0,  
    }  
  
    for item in diferencas:  
        tipo = item.get("tipo")  
        sev = item.get("severidade")  
        if tipo in contadores:  
            contadores[tipo] += 1  
        if sev in contadores:  
            contadores[sev] += 1  
    return contadores  
  
  
def classificar_acuracia(percentual):  
    if percentual > 95:  
        return {"faixa": "excelente", "cor": "verde", "descricao": "Alta aderência ao gabarito"}  
    if percentual > 80:  
        return {"faixa": "moderada", "cor": "laranja", "descricao": "Aderência intermediária, exige revisão"}  
    return {"faixa": "critica", "cor": "vermelho", "descricao": "Baixa aderência ao gabarito"}  
  
  
def gerar_resumo_executivo(percentual, total_diferencas, campos_analisados, campos_conformes):  
    if total_diferencas == 0:  
        return f"O documento foi validado com sucesso. Foram analisados {campos_analisados} campos e todos estão conformes com o gabarito."  
    if percentual > 95:  
        return f"O documento apresenta excelente aderência. Foram analisados {campos_analisados} campos, com {campos_conformes} conformes e apenas {total_diferencas} divergências."  
    if percentual > 80:  
        return f"O documento apresenta boa aderência, porém com necessidade de revisão. Foram analisados {campos_analisados} campos, com {campos_conformes} conformes e {total_diferencas} divergências."  
    return f"O documento apresenta baixa aderência ao gabarito. Foram analisados {campos_analisados} campos, com {campos_conformes} conformes e {total_diferencas} divergências relevantes."  
  
  
def top_paths_com_problema(diferencas, limite=10):  
    ordenadas = sorted(  
        diferencas,  
        key=lambda x: (  
            {"alta": 0, "media": 1, "baixa": 2}.get(x.get("severidade", "media"), 1),  
            -float(x.get("peso", 0))  
        )  
    )  
    return ordenadas[:limite]  
  
  
def gerar_melhorias_globais(diferencas, contadores):  
    melhorias = []  
  
    if contadores["faltando_no_recebido"] > 0 or contadores["item_faltando_no_recebido"] > 0:  
        melhorias.append("Implementar validação de obrigatoriedade antes do upload do JSON.")  
    if contadores["tipo_diferente"] > 0:  
        melhorias.append("Aplicar schema validation com coerção automática de tipos.")  
    if contadores["valor_diferente"] > 0:  
        melhorias.append("Reforçar normalização de texto, data, CPF/CNPJ e valores monetários.")  
    if contadores["campo_extra_no_recebido"] > 0 or contadores["item_extra_no_recebido"] > 0:  
        melhorias.append("Criar camada de saneamento para remover campos não previstos no payload.")  
    if any("[" in d.get("path", "") for d in diferencas):  
        melhorias.append("Aprimorar o matcher de listas com chave identificadora por tipo documental.")  
    if not melhorias:  
        melhorias.append("Nenhuma melhoria crítica identificada. Documento altamente aderente.")  
  
    return melhorias  
  
  
def enriquecer_diferencas(diferencas):  
    enriquecidas = []  
    for item in diferencas:  
        novo = deepcopy(item)  
        novo["sugestao_correcao"] = gerar_sugestao(item)  
        novo["melhoria_sistema"] = identificar_melhoria(item)  
        enriquecidas.append(novo)  
    return enriquecidas  
  
  
def analisar_comparacao_completa(  
    esperado,  
    recebido,  
    tipo_documental,  
    tipo_documental_legivel,  
    ged,  
    nome_arquivo,  
    gabarito_path  
):  
    diferencas, estatisticas = comparar_jsons(esperado, recebido)  
    diferencas = enriquecer_diferencas(diferencas)  
  
    contadores = gerar_contadores(diferencas)  
  
    campos_analisados = estatisticas["campos_analisados"]  
    campos_conformes = estatisticas["campos_conformes"]  
    campos_divergentes = estatisticas["campos_divergentes"]  
  
    peso_total = float(estatisticas["peso_total"]) if estatisticas["peso_total"] else 0.0  
    peso_conforme = float(estatisticas["peso_conforme"]) if estatisticas["peso_conforme"] else 0.0  
    peso_divergente = float(estatisticas["peso_divergente"]) if estatisticas["peso_divergente"] else 0.0  
    penalidade_extras = float(estatisticas["penalidade_extras"]) if estatisticas["penalidade_extras"] else 0.0  
  
    percentual_acuracia = round((peso_conforme / peso_total) * 100, 2) if peso_total > 0 else 0.0  
    classificacao = classificar_acuracia(percentual_acuracia)  
    status = "APROVADO" if len(diferencas) == 0 else "REPROVADO"  
  
    return {  
        "metadata": {  
            "tipo_documental": tipo_documental,  
            "tipo_documental_legivel": tipo_documental_legivel,  
            "ged": ged,  
            "nome_arquivo": nome_arquivo,  
            "gabarito_path": gabarito_path,  
            "data_processamento": datetime.now().strftime("%d/%m/%Y %H:%M:%S")  
        },  
        "resumo": {  
            "status": status,  
            "campos_analisados": campos_analisados,  
            "campos_conformes": campos_conformes,  
            "campos_divergentes": campos_divergentes,  
            "total_diferencas": len(diferencas),  
            "percentual_acuracia": percentual_acuracia,  
            "classificacao": classificacao,  
            "peso_total": round(peso_total, 2),  
            "peso_conforme": round(peso_conforme, 2),  
            "peso_divergente": round(peso_divergente, 2),  
            "penalidade_extras": round(penalidade_extras, 2),  
            "resumo_executivo": gerar_resumo_executivo(  
                percentual_acuracia,  
                len(diferencas),  
                campos_analisados,  
                campos_conformes  
            )  
        },  
        "contadores": contadores,  
        "top_problemas": top_paths_com_problema(diferencas, limite=10),  
        "melhorias_globais": gerar_melhorias_globais(diferencas, contadores),  
        "diferencas": diferencas  
    }  
  
  
def gerar_pdf_relatorio(analise, caminho_saida):  
    doc = SimpleDocTemplate(  
        caminho_saida,  
        pagesize=landscape(A4),  
        leftMargin=10 * mm,  
        rightMargin=10 * mm,  
        topMargin=10 * mm,  
        bottomMargin=10 * mm  
    )  
  
    styles = getSampleStyleSheet()  
    title_style = styles["Title"]  
    normal = styles["BodyText"]  
    heading = styles["Heading2"]  
  
    small = ParagraphStyle(  
        "Small",  
        parent=normal,  
        fontSize=8,  
        leading=10  
    )  
  
    elements = []  
  
    elements.append(Paragraph("Valida AI - Relatório de Validação", title_style))  
    elements.append(Spacer(1, 8))  
  
    meta_data = [  
        ["Campo", "Valor"],  
        ["Arquivo", analise["metadata"]["nome_arquivo"]],  
        ["GED", analise["metadata"]["ged"]],  
        ["Tipo documental", analise["metadata"]["tipo_documental_legivel"]],  
        ["Chave do documento", analise["metadata"]["tipo_documental"]],  
        ["Gabarito", analise["metadata"]["gabarito_path"]],  
        ["Processado em", analise["metadata"]["data_processamento"]],  
        ["Status", analise["resumo"]["status"]],  
        ["Acurácia (%)", str(analise["resumo"]["percentual_acuracia"])],  
    ]  
  
    meta_table = Table(meta_data, colWidths=[60 * mm, 180 * mm])  
    meta_table.setStyle(TableStyle([  
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D4ED8")),  
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),  
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),  
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),  
    ]))  
    elements.append(meta_table)  
    elements.append(Spacer(1, 10))  
  
    elements.append(Paragraph("Resumo Executivo", heading))  
    elements.append(Paragraph(analise["resumo"]["resumo_executivo"], normal))  
    elements.append(Spacer(1, 10))  
  
    indicadores = [  
        ["Indicador", "Valor"],  
        ["Campos analisados", str(analise["resumo"]["campos_analisados"])],  
        ["Campos conformes", str(analise["resumo"]["campos_conformes"])],  
        ["Campos divergentes", str(analise["resumo"]["campos_divergentes"])],  
        ["Total de divergências", str(analise["resumo"]["total_diferencas"])],  
        ["Peso total", str(analise["resumo"]["peso_total"])],  
        ["Peso conforme", str(analise["resumo"]["peso_conforme"])],  
        ["Peso divergente", str(analise["resumo"]["peso_divergente"])],  
        ["Penalidade por extras", str(analise["resumo"]["penalidade_extras"])],  
    ]  
  
    ind_table = Table(indicadores, colWidths=[80 * mm, 50 * mm])  
    ind_table.setStyle(TableStyle([  
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),  
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),  
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),  
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),  
    ]))  
    elements.append(ind_table)  
    elements.append(Spacer(1, 10))  
  
    elements.append(Paragraph("Top Problemas", heading))  
    top_data = [["Path", "Tipo", "Severidade", "Peso", "Correção sugerida"]]  
  
    if analise["top_problemas"]:  
        for item in analise["top_problemas"]:  
            top_data.append([  
                Paragraph(str(item["path"]), small),  
                Paragraph(str(item["tipo"]), small),  
                Paragraph(str(item["severidade"]), small),  
                Paragraph(str(item["peso"]), small),  
                Paragraph(str(item["sugestao_correcao"]), small),  
            ])  
    else:  
        top_data.append(["Sem divergências", "-", "-", "-", "-"])  
  
    top_table = Table(top_data, colWidths=[90 * mm, 40 * mm, 30 * mm, 20 * mm, 90 * mm])  
    top_table.setStyle(TableStyle([  
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7C3AED")),  
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),  
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),  
        ("VALIGN", (0, 0), (-1, -1), "TOP"),  
    ]))  
    elements.append(top_table)  
    elements.append(PageBreak())  
  
    elements.append(Paragraph("Relatório Detalhado de Divergências", heading))  
  
    detalhe_data = [[  
        "#", "Path", "Tipo", "Severidade", "Peso",  
        "Esperado", "Recebido", "Correção"  
    ]]  
  
    if analise["diferencas"]:  
        for idx, item in enumerate(analise["diferencas"], start=1):  
            detalhe_data.append([  
                str(idx),  
                Paragraph(str(item["path"]), small),  
                Paragraph(str(item["tipo"]), small),  
                Paragraph(str(item["severidade"]), small),  
                Paragraph(str(item["peso"]), small),  
                Paragraph(str(item["esperado"]), small),  
                Paragraph(str(item["recebido"]), small),  
                Paragraph(str(item["sugestao_correcao"]), small),  
            ])  
    else:  
        detalhe_data.append(["1", "Sem divergências", "-", "-", "-", "-", "-", "-"])  
  
    detalhe_table = Table(  
        detalhe_data,  
        colWidths=[10 * mm, 55 * mm, 28 * mm, 22 * mm, 15 * mm, 55 * mm, 55 * mm, 60 * mm],  
        repeatRows=1  
    )  
    detalhe_table.setStyle(TableStyle([  
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D4ED8")),  
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),  
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  
        ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),  
        ("VALIGN", (0, 0), (-1, -1), "TOP"),  
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),  
    ]))  
    elements.append(detalhe_table)  
  
    doc.build(elements)  