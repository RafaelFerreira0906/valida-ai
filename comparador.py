import os
import json
import re
import unicodedata

from difflib import SequenceMatcher

SIMILARIDADE_MINIMA = 0.75

CAMPOS_IGNORADOS = {
    "id_documento"
}

MAPA_DOCUMENTOS = {
    "e_analise_granulometrica": (
        "Análise Granulométrica",
        "analise_granulometrica"
    ),
    "e_certidao_inteiro_teor": (
        "Certidão de Inteiro Teor",
        "certidao_inteiro_teor"
    ),
    "e_contrato_de_locacao": (
        "Contrato de Locação",
        "contrato_locacao"
    ),
    "e_contrato_social": (
        "Contrato Social",
        "contrato_social"
    ),
    "e_declaracao_posse_terceiros": (
        "Declaração de Posse",
        "declaracao_posse"
    ),
    "e_demonstracoes_contabeis": (
        "Demonstrações Contábeis",
        "demonstracoes_contabeis"
    ),
    "e_fianca_bancaria": (
        "Fiança Bancária",
        "fianca_bancaria"
    ),
    "e_aditivo_fianca_bancaria": (
        "Aditivo de Fiança Bancária",
        "aditivo_fianca_bancaria"
    ),
    "e_orcamento_fne_sol": (
        "Orçamento FNE SOL",
        "orcamento_fne_sol"
    ),
    "e_parecer_gerencial": (
        "Parecer Gerencial",
        "parecer_gerencial"
    ),
    "e_procuracao": (
        "Procuração",
        "procuracao"
    ),
    "e_titulo_dominio": (
        "Título de Domínio",
        "titulo_dominio"
    )
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
                [
                    str(item)
                    for item in obj
                ]
            )

    else:

        resultado[prefix] = str(obj)

    return resultado


def carregar_json(
    caminho
):

    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(
            arquivo
        )


def localizar_campo_json(
    campo_gabarito,
    json_flat
):

    if campo_gabarito in json_flat:
        return campo_gabarito

    for chave in json_flat.keys():

        if chave.endswith(
            "." + campo_gabarito
        ):
            return chave

    for chave in json_flat.keys():

        ultimo = chave.split(".")[-1]

        if ultimo == campo_gabarito:
            return chave

    return None


def localizar_gabarito(
    tipo_documental,
    ged
):

    if tipo_documental not in MAPA_DOCUMENTOS:

        raise Exception(
            f"Tipo documental não mapeado: "
            f"{tipo_documental}"
        )

    pasta = MAPA_DOCUMENTOS[
        tipo_documental
    ][1]

    caminho = os.path.join(
        "gabaritos",
        pasta,
        f"{ged}.json"
    )

    if not os.path.exists(
        caminho
    ):

        raise Exception(
            f"Gabarito não encontrado: {caminho}"
        )

    return caminho


def comparar(
    arquivo_json
):

    json_recebido = carregar_json(
        arquivo_json
    )

    tipo_documental = next(
        iter(json_recebido)
    )

    ged = os.path.splitext(
        os.path.basename(
            arquivo_json
        )
    )[0]

    caminho_gabarito = (
        localizar_gabarito(
            tipo_documental,
            ged
        )
    )

    json_gabarito = carregar_json(
        caminho_gabarito
    )

    gabarito_flat = flatten_json(
        json_gabarito
    )

    recebido_flat = flatten_json(
        json_recebido
    )

    total = 0
    acertos = 0
    erros = 0

    divergencias = []
    nao_encontrados = []

    for campo, esperado in gabarito_flat.items():

        ultimo_campo = (
            campo.split(".")[-1]
        )

        if ultimo_campo in CAMPOS_IGNORADOS:
            continue

        total += 1

        chave_json = localizar_campo_json(
            campo,
            recebido_flat
        )

        if chave_json is None:

            erros += 1

            nao_encontrados.append(
                campo
            )

            continue

        obtido = recebido_flat[
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
                    "campo_gabarito": campo,
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

    tipo_documento = (
        MAPA_DOCUMENTOS[
            tipo_documental
        ][0]
    )

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

    for item in divergencias:

        linhas_divergencias += f"""
        <tr>
            <td>{item['campo_gabarito']}</td>
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
<h3>{tipo_documento} - GED: {id_documento}</h3>
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

<button
class="btn"
onclick="window.print()">
📄 Exportar PDF
</button>

</div>

</div>

</body>
</html>
"""