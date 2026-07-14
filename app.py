from flask import Flask, render_template, request
import os
import uuid
import comparador

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/validar", methods=["POST"])
def validar():

    try:

        excel = request.files["excel"]
        json_file = request.files["json"]

        identificador = str(uuid.uuid4())

        excel_path = os.path.join(
            UPLOAD_FOLDER,
            f"{identificador}.xlsx"
        )

       
        json_path = os.path.join(
        UPLOAD_FOLDER,
        json_file.filename
        )


        excel.save(excel_path)
        json_file.save(json_path)

        resultado = comparador.comparar(
            excel_path,
            json_path
        )

        html = comparador.gerar_relatorio_html(
            **resultado
        )

        return html

    except Exception as e:

        return f"""
        <h1>Erro na validação</h1>
        <pre>{str(e)}</pre>
        """, 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )