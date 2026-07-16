import os  
  
ALLOWED_EXTENSIONS = (".json",)  
  
# Mapeamento:  
# chave do JSON -> (nome legível, pasta dentro de gabaritos)  
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
  
  
def detectar_tipo_documental(json_data):  
    """  
    Descobre o tipo documental pela primeira chave do JSON.  
    Retorna:  
      - chave original (ex: e_contrato_social)  
      - nome legível (ex: Contrato Social)  
      - pasta do gabarito (ex: contrato_social)  
    """  
    if not isinstance(json_data, dict):  
        raise ValueError("O JSON enviado precisa ser um objeto na raiz.")  
  
    if not json_data:  
        raise ValueError("O JSON enviado está vazio.")  
  
    primeira_chave = next(iter(json_data.keys()))  
  
    if primeira_chave not in MAPEAMENTO_TIPOS:  
        chaves_validas = ", ".join(MAPEAMENTO_TIPOS.keys())  
        raise ValueError(  
            f"Tipo documental não mapeado: '{primeira_chave}'. "  
            f"Tipos aceitos: {chaves_validas}"  
        )  
  
    nome_legivel, pasta_gabarito = MAPEAMENTO_TIPOS[primeira_chave]  
    return primeira_chave, nome_legivel, pasta_gabarito  
  
  
def obter_ged_do_arquivo(nome_arquivo):  
    """  
    Extrai o GED do nome do arquivo.  
    Ex: 552776635.json -> 552776635  
    """  
    base, ext = os.path.splitext(nome_arquivo)  
  
    if ext.lower() != ".json":  
        raise ValueError("O arquivo enviado deve ter extensão .json")  
  
    ged = base.strip()  
  
    if not ged:  
        raise ValueError("Não foi possível identificar o GED pelo nome do arquivo.")  
  
    return ged  
  
  
def localizar_gabarito(base_gabaritos, pasta_gabarito, ged):  
    """  
    Localiza o gabarito em:  
      gabaritos/<pasta_gabarito>/<ged>.json  
    """  
    caminho = os.path.join(base_gabaritos, pasta_gabarito, f"{ged}.json")  
  
    if not os.path.exists(caminho):  
        raise FileNotFoundError(  
            f"Gabarito não encontrado para o GED '{ged}' em '{caminho}'."  
        )  
  
    return caminho  
  
  
def normalizar_valor(valor):  
    """  
    Normalização simples para melhorar comparação:  
    - strings: strip  
    - demais tipos: mantidos  
    """  
    if isinstance(valor, str):  
        return valor.strip()  
    return valor  
  
  
def comparar_jsons(esperado, recebido, caminho=""):  
    """  
    Compara JSON x JSON recursivamente.  
    Retorna uma lista de diferenças no formato:  
    {  
        "path": "e_contrato_social.campo.subcampo",  
        "tipo": "valor_diferente|faltando_no_recebido|campo_extra_no_recebido|tipo_diferente",  
        "esperado": ...,  
        "recebido": ...  
    }  
    """  
    diferencas = []  
  
    if type(esperado) != type(recebido):  
        diferencas.append({  
            "path": caminho or "$",  
            "tipo": "tipo_diferente",  
            "esperado": nome_tipo(esperado),  
            "recebido": nome_tipo(recebido),  
        })  
        return diferencas  
  
    if isinstance(esperado, dict):  
        chaves_esperadas = set(esperado.keys())  
        chaves_recebidas = set(recebido.keys())  
  
        # Campos faltando no recebido  
        for chave in sorted(chaves_esperadas - chaves_recebidas):  
            novo_caminho = f"{caminho}.{chave}" if caminho else chave  
            diferencas.append({  
                "path": novo_caminho,  
                "tipo": "faltando_no_recebido",  
                "esperado": esperado[chave],  
                "recebido": None,  
            })  
  
        # Campos extras no recebido  
        for chave in sorted(chaves_recebidas - chaves_esperadas):  
            novo_caminho = f"{caminho}.{chave}" if caminho else chave  
            diferencas.append({  
                "path": novo_caminho,  
                "tipo": "campo_extra_no_recebido",  
                "esperado": None,  
                "recebido": recebido[chave],  
            })  
  
        # Campos em comum  
        for chave in sorted(chaves_esperadas & chaves_recebidas):  
            novo_caminho = f"{caminho}.{chave}" if caminho else chave  
            diferencas.extend(  
                comparar_jsons(  
                    esperado[chave],  
                    recebido[chave],  
                    novo_caminho  
                )  
            )  
  
        return diferencas  
  
    if isinstance(esperado, list):  
        tamanho_esperado = len(esperado)  
        tamanho_recebido = len(recebido)  
        maior = max(tamanho_esperado, tamanho_recebido)  
  
        for i in range(maior):  
            novo_caminho = f"{caminho}[{i}]"  
  
            if i >= tamanho_esperado:  
                diferencas.append({  
                    "path": novo_caminho,  
                    "tipo": "item_extra_no_recebido",  
                    "esperado": None,  
                    "recebido": recebido[i],  
                })  
            elif i >= tamanho_recebido:  
                diferencas.append({  
                    "path": novo_caminho,  
                    "tipo": "item_faltando_no_recebido",  
                    "esperado": esperado[i],  
                    "recebido": None,  
                })  
            else:  
                diferencas.extend(  
                    comparar_jsons(  
                        esperado[i],  
                        recebido[i],  
                        novo_caminho  
                    )  
                )  
  
        return diferencas  
  
    # Tipos primitivos  
    valor_esperado = normalizar_valor(esperado)  
    valor_recebido = normalizar_valor(recebido)  
  
    if valor_esperado != valor_recebido:  
        diferencas.append({  
            "path": caminho or "$",  
            "tipo": "valor_diferente",  
            "esperado": esperado,  
            "recebido": recebido,  
        })  
  
    return diferencas  
  
  
def nome_tipo(valor):  
    if valor is None:  
        return "null"  
    return type(valor).__name__  
  
  
def gerar_resumo(diferencas):  
    resumo = {  
        "total_diferencas": len(diferencas),  
        "valor_diferente": 0,  
        "faltando_no_recebido": 0,  
        "campo_extra_no_recebido": 0,  
        "tipo_diferente": 0,  
        "item_extra_no_recebido": 0,  
        "item_faltando_no_recebido": 0,  
        "status": "APROVADO"  
    }  
  
    for item in diferencas:  
        tipo = item.get("tipo")  
        if tipo in resumo:  
            resumo[tipo] += 1  
  
    if resumo["total_diferencas"] > 0:  
        resumo["status"] = "REPROVADO"  
  
    return resumo  