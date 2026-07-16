import os
import json
import re
import unicodedata
import html

from difflib import SequenceMatcher


SIMILARIDADE_MINIMA = 0.75

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CAMPOS_IGNORADOS = {
    "id_documento"
}


MAPA_DOCUMENTOS = {
    "e_analise_granulometrica": {
        "nome": "Análise Granulométrica",
        "pasta": "analise_granulometrica"
    },
    "e_certidao_inteiro_teor": {
        "nome": "Certidão de Inteiro Teor",
        "pasta": "certidao_inteiro_teor"
    },
    "e_contrato_de_locacao": {
        "nome": "Contrato de Locação",
        "pasta": "contrato_locacao"
    },
    "e_contrato_social": {
        "nome": "Contrato Social",
        "pasta": "contrato_social"
    },
    "e_declaracao_posse_terceiros": {
        "nome": "Declaração de Posse",
        "pasta": "declaracao_posse"
    },
    "e_demonstracoes_contabeis": {
        "nome": "Demonstrações Contábeis",
        "pasta": "demonstracoes_contabeis"
    },
    "e_fianca_bancaria": {
        "nome": "Fiança Bancária",
        "pasta": "fianca_bancaria"
    },
    "e_aditivo_fianca_bancaria": {
        "nome": "Aditivo de Fiança Bancária",
        "pasta": "aditivo_fianca_bancaria"
    },
    "e_orcamento_fne_sol": {
        "nome": "Orçamento FNE SOL",
        "pasta": "orcamento_fne_sol"
    },
    "e_parecer_gerencial": {
        "nome": "Parecer Gerencial",
        "pasta": "parecer_gerencial"
    },
    "e_procuracao": {
        "nome": "Procuração",
        "pasta": "procuracao"
    },
    "e_titulo_dominio": {
        "nome": "Título de Domínio",
        "pasta": "titulo_dominio"
    }
}


def escapar(valor):
    if valor is None:
        return ""

    return html.escape(str(valor))


def normalizar(texto):
    if texto is None:
        return ""

    texto = str(texto)

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    texto = texto.encode(
        "ASCII",
        "ignore"
    ).decode(
        "ASCII"
    )

    texto = texto.lower()

    texto = re.sub(
        r"[^\w\s]",
        "",
        texto
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


def calcular_similaridade(esperado, obtido):
    esperado_normalizado = normalizar(esperado)
    obtido_normalizado = normalizar(obtido)

    return SequenceMatcher(
        None,
        esperado_normalizado,
        obtido_normalizado
    ).ratio()


def comparar_textos(esperado, obtido):
    esperado_normalizado = normalizar(esperado)
    obtido_normalizado = normalizar(obtido)

    if esperado_normalizado == obtido_normalizado:
        return True

    if esperado_normalizado == "" or obtido_normalizado == "":
        return False

    if esperado_normalizado in obtido_normalizado:
        return True

    if obtido_normalizado in esperado_normalizado:
        return True

    score = SequenceMatcher(
        None,
        esperado_normalizado,
        obtido_normalizado
    ).ratio()

    return score >= SIMILARIDADE_MINIMA


def flatten_json(objeto, prefixo=""):
    resultado = {}

    if isinstance(objeto, dict):
        for chave, valor in objeto.items():
            novo_prefixo = (
                f"{prefixo}.{chave}"
                if prefixo
                else chave
            )

            resultado.update(
                flatten_json(
                    valor,
                    novo_prefixo
                )
            )

    elif isinstance(objeto, list):
        if len(objeto) == 0:
            resultado[prefixo] = ""

        else:
            for indice, item in enumerate(objeto):
                novo_prefixo = f"{prefixo}[{indice}]"

                if isinstance(item, dict) or isinstance(item, list):
                    resultado.update(
                        flatten_json(
                            item,
                            novo_prefixo
                        )
                    )
                else:
                    resultado[novo_prefixo] = str(item)

    else:
        resultado[prefixo] = "" if objeto is None else str(objeto)

    return resultado


def carregar_json(caminho):
    try:
        with open(
            caminho,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)

    except json.JSONDecodeError as erro:
        raise Exception(
            f"JSON inválido no arquivo {os.path.basename(caminho)}. "
            f"Detalhe: {str(erro)}"
        )


def obter_tipo_documental(json_dados):
    if not isinstance(json_dados, dict):
        raise Exception(
            "O JSON enviado deve possuir um objeto na raiz."
        )

    if len(json_dados.keys()) == 0:
        raise Exception(
            "O JSON enviado está vazio."
        )

    return next(iter(json_dados))


def obter_ged(caminho_json):
    nome_arquivo = os.path.basename(caminho_json)

    ged = os.path.splitext(nome_arquivo)[0]

    if not ged:
        raise Exception(
            "Não foi possível identificar o GED pelo nome do arquivo."
        )

    return ged


def localizar_gabarito(tipo_documental, ged):
    if tipo_documental not in MAPA_DOCUMENTOS:
        raise Exception(
            f"Tipo documental não mapeado: {tipo_documental}"
        )

    pasta = MAPA_DOCUMENTOS[tipo_documental]["pasta"]

    caminho_gabarito = os.path.join(
        BASE_DIR,
        "gabaritos",
        pasta,
        f"{ged}.json"
    )

    if not os.path.exists(caminho_gabarito):
        raise Exception(
            "Gabarito não encontrado.\n\n"
            f"Tipo documental: {tipo_documental}\n"
            f"GED: {ged}\n"
            f"Caminho procurado: {caminho_gabarito}"
        )

    return caminho_gabarito


def campo_ignorado(campo):
    ultimo_campo = campo.split(".")[-1]

    ultimo_campo = re.sub(
        r"\[\d+\]",
        "",
        ultimo_campo
    )

    return ultimo_campo in CAMPOS_IGNORADOS


def localizar_campo_json(campo_gabarito, json_recebido_flat):
    if campo_gabarito in json_recebido_flat:
        return campo_gabarito

    for chave in json_recebido_flat.keys():
        if chave.endswith("." + campo_gabarito):
            return chave

    ultimo_gabarito = campo_gabarito.split(".")[-1]

    for chave in json_recebido_flat.keys():
        ultimo_json = chave.split(".")[-1]

        if ultimo_json == ultimo_gabarito:
            return chave

    return None


def comparar(caminho_json_recebido):
    json_recebido = carregar_json(caminho_json_recebido)

    tipo_documental = obter_tipo_documental(json_recebido)

    ged = obter_ged(caminho_json_recebido)

    caminho_gabarito = localizar_gabarito(
        tipo_documental,
        ged
    )

    json_gabarito = carregar_json(caminho_gabarito)

    recebido_flat = flatten_json(json_recebido)
    gabarito_flat = flatten_json(json_gabarito)

    total = 0
    acertos = 0
    erros = 0

    divergencias = []
    nao_encontrados = []

    for campo_gabarito, valor_esperado in gabarito_flat.items():
        if campo_ignorado(campo_gabarito):
            continue

        total += 1

        campo_json = localizar_campo_json(
            campo_gabarito,
            recebido_flat
        )

        if campo_json is None:
            erros += 1

            nao_encontrados.append(
                campo_gabarito
            )

            continue

        valor_obtido = recebido_flat[campo_json]

        if comparar_textos(
            valor_esperado,
            valor_obtido
        ):
            acertos += 1

        else:
            erros += 1

            similaridade = calcular_similaridade(
                valor_esperado,
                valor_obtido
            )

            divergencias.append(
                {
                    "campo_gabarito": campo_gabarito,
                    "campo_json": campo_json,
                    "esperado": valor_esperado,
                    "obtido": valor_obtido,
                    "similaridade": round(
                        similaridade * 100,
                        2
                    )
                }
            )

    percentual = (
        (acertos / total) * 100
        if total > 0
        else 0
    )

    tipo_documento = MAPA_DOCUMENTOS[tipo_documental]["nome"]

    return {
        "total": total,
        "acertos": acertos,
        "erros": erros,
        "percentual": percentual,
        "divergencias": divergencias,
        "nao_encontrados": nao_encontrados,
        "tipo_documento": tipo_documento,
        "id_documento": ged
    }


def gerar_relatorio_html(
    total,
    acertos,
    erros,
    percentual,
    divergencias,
    nao_encontrados,
    tipo_documento,
    id_documento
):
    if percentual >= 95:
        cor_acuracia = "#09FA96"
    elif percentual >= 80:
        cor_acuracia = "#FF9800"
    else:
        cor_acuracia = "#D32F2F"

    linhas_divergencias = ""

    if len(divergencias) == 0:
        linhas_divergencias = """
        <tr>
            <td colspan="5">Nenhuma divergência encontrada.</td>
        </tr>
        """
    else:
        for item in divergencias:
            linhas_divergencias += f"""
            <tr>
                <td>{escapar(item['campo_gabarito'])}</td>
                <td>{escapar(item['campo_json'])}</td>
                <td>{escapar(item['esperado'])}</td>
                <td>{escapar(item['obtido'])}</td>
                <td>{escapar(item['similaridade'])}%</td>
            </tr>
            """

    linhas_nao_encontrados = ""

    if len(nao_encontrados) == 0:
        linhas_nao_encontrados = """
        <tr>
            <td colspan="2">Nenhum campo ausente encontrado.</td>
        </tr>
        """
    else:
        for campo in nao_encontrados:
            linhas_nao_encontrados += f"""
            <tr>
                <td>{escapar(campo)}</td>
                <td>CAMPO NÃO ENCONTRADO</td>
            </tr>
            """

    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Valida AI</title>

<style>

body {{
    margin: 0;
    background: #F5F5F5;
    font-family: 'Segoe UI', Arial, sans-serif;
}}

.topo {{
    background: #AC123B;
    color: white;
    padding: 25px;
}}

.topo h1 {{
    margin: 0;
}}

.topo h3 {{
    margin-bottom: 0;
}}

.container {{
    width: 95%;
    margin: auto;
}}

.card {{
    background: white;
    margin-top: 20px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,.10);
}}

.indicadores {{
    display: flex;
    gap: 40px;
    flex-wrap: wrap;
}}

.indicador {{
    min-width: 140px;
}}

.indicador strong {{
    color: #AC123B;
}}

.barra {{
    width: 100%;
    height: 35px;
    background: #DDD;
    margin-top: 20px;
    border-radius: 8px;
    overflow: hidden;
}}

.barra-interna {{
    width: {percentual}%;
    height: 100%;
    background: {cor_acuracia};
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}}

th {{
    background: #AC123B;
    color: white;
}}

th, td {{
    border: 1px solid #DDD;
    padding: 10px;
    text-align: center;
    vertical-align: top;
}}

.btn {{
    background: #F58220;
    color: white;
    border: none;
    padding: 14px 30px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
}}

.btn-voltar {{
    background: #AC123B;
    color: white;
    border: none;
    padding: 14px 30px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    margin-right: 10px;
}}

.footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 40px;
    padding: 20px;
    border-top: 1px solid #DDD;
}}

.footer-esquerda {{
    font-weight: bold;
}}

.footer-direita {{
    font-weight: bold;
    color: #AC123B;
}}

@media print {{
    .btn,
    .btn-voltar {{
        display: none;
    }}
}}

</style>
</head>

<body>

<div class="topo">
    <h1>Valida AI</h1>
    <h3>{escapar(tipo_documento)} - GED: {escapar(id_documento)}</h3>
</div>

<div class="container">

    <div class="card">
        <h2>Resumo da Validação</h2>

        <div class="indicadores">

            <div class="indicador">
                <strong>Campos Avaliados</strong><br>
                {total}
            </div>

            <div class="indicador">
                <strong>Acertos</strong><br>
                {acertos}
            </div>

            <div class="indicador">
                <strong>Erros</strong><br>
                {erros}
            </div>

            <div class="indicador">
                <strong>Acurácia</strong><br>
                {percentual:.2f}%
            </div>

        </div>

        <div class="barra">
            <div class="barra-interna"></div>
        </div>
    </div>

    <div class="card">
        <h2>Campos Divergentes</h2>

        <table>
            <thead>
                <tr>
                    <th>Campo Gabarito</th>
                    <th>Campo JSON</th>
                    <th>Esperado</th>
                    <th>Obtido</th>
                    <th>Similaridade</th>
                </tr>
            </thead>

            <tbody>
                {linhas_divergencias}
            </tbody>
        </table>
    </div>

    <div class="card">
        <h2>Campos Não Encontrados</h2>

        <table>
            <thead>
                <tr>
                    <th>Campo</th>
                    <th>Status</th>
                </tr>
            </thead>

            <tbody>
                {linhas_nao_encontrados}
            </tbody>
        </table>
    </div>

    <div style="text-align:center;margin:30px;">
        <button class="btn-voltar" onclick="window.location.href='/'">
            Nova Validação
        </button>

        <button class="btn" onclick="window.print()">
            📄 Exportar PDF
        </button>
    </div>

    <div class="footer">
        <div class="footer-esquerda">
            Valida AI - Resultado da Validação
        </div>

        <div class="footer-direita">
            Desenvolvido por Rafael Ferreira
        </div>
    </div>

</div>

</body>
</html>
"""