from flask import Flask, render_template, request
import os

import comparador

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@app.route("/")
def inicio():
    return render_template(
        "index.html"
    )


@app.route(
    "/validar",
    methods=["POST"]
)
def validar():

    try:

        arquivo_json = request.files.get(
            "json"
        )

        if not arquivo_json:
            raise Exception(
                "Nenhum arquivo JSON foi enviado."
            )

        nome_arquivo = os.path.basename(
            arquivo_json.filename
        )

        if nome_arquivo == "":
            raise Exception(
                "Nenhum arquivo foi selecionado."
            )

        if not nome_arquivo.lower().endswith(
            ".json"
        ):
            raise Exception(
                "O arquivo enviado deve ser JSON."
            )

        caminho_json = os.path.join(
            UPLOAD_FOLDER,
            nome_arquivo
        )

        arquivo_json.save(
            caminho_json
        )

        resultado = comparador.comparar(
            caminho_json
        )

        return comparador.gerar_relatorio_html(
            **resultado
        )

    except Exception as erro:

        return f"""
        <html>
        <body style="font-family:Segoe UI;padding:40px">

            <h2>Erro na validação</h2>

            <pre>{str(erro)}</pre>

            <br>

            <button onclick="history.back()">
                Voltar
            </button>

        </body>
        </html>
        """, 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )