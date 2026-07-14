import os
import json
import re
import unicodedata
import pandas as pd

from difflib import SequenceMatcher


SIMILARIDADE_MINIMA = 0.75

CAMPOS_IGNORADOS = {
    "id_documento"
}

MAPA_DOCUMENTOS = {

    "e_analise_granulometrica":
        "Análise Granulométrica",

    "e_certidao_inteiro_teor":
        "Certidão de Inteiro Teor",

    "e_contrato_de_locacao":
        "Contrato de Locação",

    "e_contrato_social":
        "Contrato Social",

    "e_declaracao_posse_terceiros":
        "Declaração de Posse",

    "e_demonstracoes_contabeis":
        "Demonstrações Contábeis",

    "e_fianca_bancaria":
        "Fiança Bancária",

    "e_aditivo_fianca_bancaria":
        "Aditivo de Fiança Bancária",

    "e_orcamento_fne_sol":
        "Orçamento FNE SOL",

    "e_parecer_gerencial":
        "Parecer Gerencial",

    "e_procuracao":
        "Procuração",

    "e_titulo_dominio":
        "Título de Domínio"

}


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


def comparar_textos(
    esperado,
    obtido
):

    esperado = normalizar(
        esperado
    )

    obtido = normalizar(
        obtido
    )

    if esperado == obtido:
        return True

    if esperado in obtido:
        return True

    if obtido in esperado:
        return True

    score = SequenceMatcher(
        None,
        esperado,
        obtido
    ).ratio()

    return score >= SIMILARIDADE_MINIMA


def flatten_json(
    obj,
    prefix=""
):

    resultado = {}

    if isinstance(obj, dict):

        for chave, valor in obj.items():

            novo_prefixo = (
                f"{prefix}.{chave}"
                if prefix
                else chave
            )

            resultado.update(
                flatten_json(
                    valor,
                    novo_prefixo
                )
            )

    elif isinstance(obj, list):

        if len(obj) == 0:

            resultado[prefix] = ""

        else:

            resultado[prefix] = " | ".join(
                [str(x) for x in obj]
            )

    else:

        resultado[prefix] = str(obj)

    return resultado


def carregar_gabarito(
    arquivo_excel
):

    df = pd.read_excel(
        arquivo_excel,
        engine="openpyxl"
    )

    if (
        "Campo" not in df.columns
        or
        "Valor" not in df.columns
    ):
        raise Exception(
            "O Excel deve possuir as colunas Campo e Valor."
        )

    gabarito = {}

    for _, linha in df.iterrows():

        campo = str(
            linha["Campo"]
        ).strip()

        valor = ""

        if pd.notna(
            linha["Valor"]
        ):
            valor = str(
                linha["Valor"]
            ).strip()

        gabarito[campo] = valor

    return gabarito


def carregar_json(
    arquivo_json
):

    with open(
        arquivo_json,
        "r",
        encoding="utf-8"
    ) as f:

        dados = json.load(f)

    return flatten_json(
        dados
    )


def localizar_campo_json(
    campo_excel,
    json_flat
):

    if campo_excel in json_flat:
        return campo_excel

    for chave in json_flat.keys():

        if chave.endswith(
            "." + campo_excel
        ):
            return chave

    for chave in json_flat.keys():

        ultimo = chave.split(".")[-1]

        if ultimo == campo_excel:
            return chave

    return None


def comparar(
    arquivo_excel,
    arquivo_json
):

    gabarito = carregar_gabarito(
        arquivo_excel
    )

    resultado_json = carregar_json(
        arquivo_json
    )

    with open(
        arquivo_json,
        "r",
        encoding="utf-8"
    ) as f:

        json_original = json.load(f)

    total = 0
    acertos = 0
    erros = 0

    divergencias = []
    nao_encontrados = []

    for campo, esperado in gabarito.items():

        if campo in CAMPOS_IGNORADOS:
            continue

        total += 1

        chave_json = localizar_campo_json(
            campo,
            resultado_json
        )

        if chave_json is None:

            erros += 1

            nao_encontrados.append(
                campo
            )

            continue

        obtido = resultado_json[
            chave_json
        ]

        if comparar_textos(
            esperado,
            obtido
        ):

            acertos += 1

        else:

            erros += 1

            score = SequenceMatcher(
                None,
                normalizar(
                    esperado
                ),
                normalizar(
                    obtido
                )
            ).ratio()

            divergencias.append(
                {
                    "campo_excel": campo,
                    "campo_json": chave_json,
                    "esperado": esperado,
                    "obtido": obtido,
                    "similaridade": round(
                        score * 100,
                        2
                    )
                }
            )

    percentual = (
        (acertos / total) * 100
        if total > 0
        else 0
    )

    id_documento = os.path.splitext(
        os.path.basename(
            arquivo_json
        )
    )[0]

    primeira_chave = next(
        iter(json_original)
    )

    tipo_documento = MAPA_DOCUMENTOS.get(
        primeira_chave,
        primeira_chave
            .replace("e_", "")
            .replace("_", " ")
            .title()
    )

    return {
        "total": total,
        "acertos": acertos,
        "erros": erros,
        "percentual": percentual,
        "divergencias": divergencias,
        "nao_encontrados": nao_encontrados,
        "tipo_documento": tipo_documento,
        "id_documento": id_documento
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

    for item in divergencias:

        linhas_divergencias += f"""
        <tr>
            <td>{item['campo_excel']}</td>
            <td>{item['campo_json']}</td>
            <td>{item['esperado']}</td>
            <td>{item['obtido']}</td>
            <td>{item['similaridade']}%</td>
        </tr>
        """

    linhas_nao_encontrados = ""

    for campo in nao_encontrados:

        linhas_nao_encontrados += f"""
        <tr>
            <td>{campo}</td>
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
    margin:0;
    background:#F5F5F5;
    font-family:'Segoe UI', Arial, sans-serif;
}}

.topo {{
    background:#AC123B;
    color:white;
    padding:25px;
}}

.container {{
    width:95%;
    margin:auto;
}}

.card {{
    background:white;
    margin-top:20px;
    padding:20px;
    border-radius:8px;
    box-shadow:0 2px 4px rgba(0,0,0,.10);
}}

.indicadores {{
    display:flex;
    gap:40px;
    flex-wrap:wrap;
}}

.barra {{
    width:100%;
    height:35px;
    background:#DDD;
    margin-top:20px;
    border-radius:8px;
}}

.barra-interna {{
    width:{percentual}%;
    height:100%;
    background:{cor_acuracia};
}}

table {{
    width:100%;
    border-collapse:collapse;
}}

th {{
    background:#AC123B;
    color:white;
}}

th, td {{
    border:1px solid #DDD;
    padding:10px;
    text-align:center;
}}

.btn {{
    background:#F58220;
    color:white;
    border:none;
    padding:14px 30px;
    border-radius:6px;
    cursor:pointer;
    font-weight:bold;
}}

.footer {{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-top:40px;
    padding:20px;
    border-top:1px solid #DDD;
}}

.footer-esquerda {{
    font-weight:bold;
}}

.footer-direita {{
    font-weight:bold;
    color:#AC123B;
}}

@media print {{

    .btn {{
        display:none;
    }}

}}

</style>

</head>

<body>

<div class="topo">

<h1>Valida AI</h1>

<h3>
{tipo_documento} - GED: {id_documento}
</h3>

</div>

<div class="container">

<div class="card">

<h2>Resumo da Validação</h2>

<div class="indicadores">

<div>
<strong>Campos Avaliados</strong><br>
{total}
</div>

<div>
<strong>Acertos</strong><br>
{acertos}
</div>

<div>
<strong>Erros</strong><br>
{erros}
</div>

<div>
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
<th>Campo Excel</th>
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

<button
class="btn"
onclick="window.print()">
📄 Exportar PDF
</button>

</div>

<div class="footer">

<div class="footer-esquerda">
Valida AI - Resultado da Validação
</div>

<div class="footer-direita">
Desenvolvido por: Rafael Ferreira - D004028
</div>

</div>

</div>

</body>
</html>
"""
