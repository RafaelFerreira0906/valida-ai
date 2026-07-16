import os  
import json  
import uuid  
from flask import Flask, render_template, request, send_file  
from werkzeug.utils import secure_filename  
  
from comparador import (  
    ALLOWED_EXTENSIONS,  
    detectar_tipo_documental,  
    obter_ged_do_arquivo,  
    localizar_gabarito,  
    analisar_comparacao_completa,  
    gerar_excel_relatorio  
)  
  
app = Flask(__name__)  
  
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
UPLOAD_FOLDER = os.path.join("/tmp", "uploads")  
REPORTS_FOLDER = os.path.join("/tmp", "reports")  
GABARITOS_DIR = os.path.join(BASE_DIR, "gabaritos")  
  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  
os.makedirs(REPORTS_FOLDER, exist_ok=True)  
  
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER  
app.config["REPORTS_FOLDER"] = REPORTS_FOLDER  
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB  
  
REPORT_CACHE = {}  
  
  
@app.route("/", methods=["GET", "POST"])  
def index():  
    contexto = {  
        "erro": None,  
        "sucesso": None,  
        "analise": None,  
        "tipo_documental": None,  
        "tipo_documental_legivel": None,  
        "ged": None,  
        "gabarito_path": None,  
        "nome_arquivo": None,  
        "report_id": None  
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
  
        try:  
            arquivo.save(caminho_upload)  
        except Exception as e:  
            contexto["erro"] = f"Erro ao salvar o arquivo enviado: {str(e)}"  
            return render_template("index.html", **contexto)  
  
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
  
            analise = analisar_comparacao_completa(  
                esperado=json_gabarito,  
                recebido=json_enviado,  
                tipo_documental=tipo_documental,  
                tipo_documental_legivel=tipo_documental_legivel,  
                ged=ged,  
                nome_arquivo=nome_arquivo,  
                gabarito_path=contexto["gabarito_path"]  
            )  
  
            report_id = str(uuid.uuid4())  
            arquivo_excel = os.path.join(  
                app.config["REPORTS_FOLDER"],  
                f"relatorio_{ged}_{report_id}.xlsx"  
            )  
            gerar_excel_relatorio(analise, arquivo_excel)  
  
            REPORT_CACHE[report_id] = {  
                "excel_path": arquivo_excel,  
                "filename": f"relatorio_validacao_{ged}.xlsx"  
            }  
  
            contexto["analise"] = analise  
            contexto["report_id"] = report_id  
            contexto["sucesso"] = "Comparação realizada com sucesso."  
  
        except FileNotFoundError as e:  
            contexto["erro"] = str(e)  
        except ValueError as e:  
            contexto["erro"] = str(e)  
        except Exception as e:  
            contexto["erro"] = f"Erro inesperado durante o processamento: {str(e)}"  
  
    return render_template("index.html", **contexto)  
  
  
@app.route("/download/excel/<report_id>")  
def download_excel(report_id):  
    report = REPORT_CACHE.get(report_id)  
  
    if not report:  
        return "Relatório não encontrado ou expirado.", 404  
  
    excel_path = report["excel_path"]  
    download_name = report["filename"]  
  
    if not os.path.exists(excel_path):  
        return "Arquivo do relatório não encontrado.", 404  
  
    return send_file(  
        excel_path,  
        as_attachment=True,  
        download_name=download_name,  
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  
    )  
  
  
if __name__ == "__main__":  
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)  