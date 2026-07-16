import os  
import json  
from flask import Flask, render_template, request  
from werkzeug.utils import secure_filename  
  
from comparador import (  
    ALLOWED_EXTENSIONS,  
    detectar_tipo_documental,  
    obter_ged_do_arquivo,  
    localizar_gabarito,  
    comparar_jsons,  
    gerar_resumo  
)  
  
app = Flask(__name__)  
  
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
UPLOAD_FOLDER = os.path.join("/tmp", "uploads")  
GABARITOS_DIR = os.path.join(BASE_DIR, "gabaritos")  
  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  
  
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER  
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB  
  
  
@app.route("/", methods=["GET", "POST"])  
def index():  
    contexto = {  
        "erro": None,  
        "sucesso": None,  
        "resultado": None,  
        "resumo": None,  
        "tipo_documental": None,  
        "tipo_documental_legivel": None,  
        "ged": None,  
        "gabarito_path": None,  
        "nome_arquivo": None  
    }  
  
    if request.method == "POST":  
        if "arquivo_json" not in request.files:  
            contexto["erro"] = "Nenhum arquivo foi enviado."  
            return render_template("index.html", **contexto)  
  
        arquivo = request.files["arquivo_json"]  
  
        if arquivo.filename == "":  
            contexto["erro"] = "Selecione um arquivo JSON."  
            return render_template("index.html", **contexto)  
  
        nome_arquivo = secure_filename(arquivo.filename)  
        contexto["nome_arquivo"] = nome_arquivo  
  
        if not nome_arquivo.lower().endswith(ALLOWED_EXTENSIONS):  
            contexto["erro"] = "Arquivo inválido. Envie um arquivo .json."  
            return render_template("index.html", **contexto)  
  
        caminho_upload = os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo)  
        arquivo.save(caminho_upload)  
  
        try:  
            with open(caminho_upload, "r", encoding="utf-8") as f:  
                json_enviado = json.load(f)  
        except json.JSONDecodeError:  
            contexto["erro"] = "O arquivo enviado não contém um JSON válido."  
            return render_template("index.html", **contexto)  
        except Exception as e:  
            contexto["erro"] = f"Erro ao ler o arquivo enviado: {str(e)}"  
            return render_template("index.html", **contexto)  
  
        try:  
            tipo_documental, tipo_documental_legivel, pasta_gabarito = detectar_tipo_documental(json_enviado)  
            ged = obter_ged_do_arquivo(nome_arquivo)  
            caminho_gabarito = localizar_gabarito(GABARITOS_DIR, pasta_gabarito, ged)  
  
            contexto["tipo_documental"] = tipo_documental  
            contexto["tipo_documental_legivel"] = tipo_documental_legivel  
            contexto["ged"] = ged  
            contexto["gabarito_path"] = os.path.relpath(caminho_gabarito, BASE_DIR)  
  
            with open(caminho_gabarito, "r", encoding="utf-8") as f:  
                json_gabarito = json.load(f)  
  
            diferencas = comparar_jsons(  
                esperado=json_gabarito,  
                recebido=json_enviado  
            )  
  
            resumo = gerar_resumo(diferencas)  
  
            contexto["resultado"] = diferencas  
            contexto["resumo"] = resumo  
            contexto["sucesso"] = "Comparação realizada com sucesso."  
  
        except FileNotFoundError as e:  
            contexto["erro"] = str(e)  
        except ValueError as e:  
            contexto["erro"] = str(e)  
        except Exception as e:  
            contexto["erro"] = f"Erro inesperado durante o processamento: {str(e)}"  
  
    return render_template("index.html", **contexto)  
  
  
if __name__ == "__main__":  
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)  