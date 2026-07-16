from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

import comparador


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/validar", methods=["POST"])
def validar():
    try:
        arquivo_json = request.files.get("json")

        if arquivo_json is None:
            raise Exception("Nenhum arquivo foi enviado.")

        if arquivo_json.filename == "":
            raise Exception("Nenhum arquivo foi selecionado.")

        nome_arquivo = secure_filename(arquivo_json.filename)

        if not nome_arquivo.lower().endswith(".json"):
            raise Exception("O arquivo enviado deve estar no formato .json.")

        caminho_json = os.path.join(
            app.config["UPLOAD_FOLDER"],
            nome_arquivo
        )

        arquivo_json.save(caminho_json)

        resultado = comparador.comparar(caminho_json)

        return comparador.gerar_relatorio_html(**resultado)

    except Exception as erro:
        return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Erro - Valida AI</title>

<style>
body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #f4f4f4;
    padding: 50px;
}}

.card {{
    background: white;
    max-width: 800px;
    margin: auto;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,.1);
}}

h1 {{
    color: #AC123B;
}}

pre {{
    background: #f5f5f5;
    padding: 15px;
    border-radius: 6px;
    white-space: pre-wrap;
}}

button {{
    background: #AC123B;
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
}}
</style>
</head>

<body>
<div class="card">
    <h1>Erro na validação</h1>
    <pre>{str(erro)}</pre>

    <button onclick="window.location.href='/'">
        Voltar
    </button>
</div>
</body>
</html>
        """, 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )