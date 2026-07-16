import os  
import json  
import uuid  
import time  
  
from flask import Flask, render_template, request, send_file  
from werkzeug.utils import secure_filename  
  
from comparador import (  
    ALLOWED_EXTENSIONS,  
    detectar_tipo_documental,  
    obter_id_documento_do_arquivo,  
    localizar_gabarito,  
    analisar_comparacao_completa,  
    gerar_pdf_relatorio  
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
        "report_id": None,  
        "json_texto": "",  
        "id_documento_manual": ""  
    }  
  
    if request.method == "POST":  
        inicio = time.perf_counter()  
  
        arquivo = request.files.get("arquivo_json")  
        json_texto = request.form.get("json_texto", "").strip()  
        id_documento_manual = request.form.get("id_documento_manual", "").strip()  
  
        contexto["json_texto"] = json_texto  
        contexto["id_documento_manual"] = id_documento_manual  
  
        json_enviado = None  
        nome_arquivo_original = None  
        id_documento = None  
        origem_entrada = None  
  
        try:  
            # Prioridade para JSON colado  
            if json_texto:  
                origem_entrada = "json_colado"  
  
                try:  
                    json_enviado = json.loads(json_texto)  
                except json.JSONDecodeError as e:  
                    contexto["erro"] = f"JSON colado inválido: {str(e)}"  
                    return render_template("index.html", **contexto)  
  
                if not id_documento_manual:  
                    contexto["erro"] = "Ao colar o JSON, informe também o ID do documento."  
                    return render_template("index.html", **contexto)  
  
                id_documento = id_documento_manual  
                nome_arquivo_original = f"{id_documento}.json"  
  
            else:  
                if not arquivo or arquivo.filename == "":  
                    contexto["erro"] = "Envie um arquivo JSON ou cole o conteúdo do JSON no campo de texto."  
                    return render_template("index.html", **contexto)  
  
                origem_entrada = "arquivo_upload"  
                nome_arquivo_original = secure_filename(arquivo.filename)  
  
                if not nome_arquivo_original.lower().endswith(ALLOWED_EXTENSIONS):  
                    contexto["erro"] = "Arquivo inválido. Envie um arquivo .json."  
                    return render_template("index.html", **contexto)  
  
                id_documento = obter_id_documento_do_arquivo(nome_arquivo_original)  
  
                nome_interno = f"{uuid.uuid4()}_{nome_arquivo_original}"  
                caminho_upload = os.path.join(app.config["UPLOAD_FOLDER"], nome_interno)  
                arquivo.save(caminho_upload)  
  
                try:  
                    with open(caminho_upload, "r", encoding="utf-8") as f:  
                        json_enviado = json.load(f)  
                except json.JSONDecodeError:  
                    contexto["erro"] = "O arquivo enviado não contém um JSON válido."  
                    return render_template("index.html", **contexto)  
  
            tipo_documental, tipo_documental_legivel, pasta_gabarito = detectar_tipo_documental(json_enviado)  
            caminho_gabarito = localizar_gabarito(GABARITOS_DIR, pasta_gabarito, id_documento)  
  
            with open(caminho_gabarito, "r", encoding="utf-8") as f:  
                json_gabarito = json.load(f)  
  
            tempo_processamento_ms = round((time.perf_counter() - inicio) * 1000, 2)  
  
            analise = analisar_comparacao_completa(  
                esperado=json_gabarito,  
                recebido=json_enviado,  
                tipo_documental=tipo_documental,  
                tipo_documental_legivel=tipo_documental_legivel,  
                id_documento=id_documento,  
                nome_arquivo=nome_arquivo_original,  
                gabarito_path=os.path.relpath(caminho_gabarito, BASE_DIR),  
                origem_entrada=origem_entrada,  
                tempo_processamento_ms=tempo_processamento_ms  
            )  
  
            report_id = str(uuid.uuid4())  
            pdf_path = os.path.join(  
                app.config["REPORTS_FOLDER"],  
                f"relatorio_{id_documento}_{report_id}.pdf"  
            )  
  
            gerar_pdf_relatorio(analise, pdf_path)  
  
            REPORT_CACHE[report_id] = {  
                "pdf_path": pdf_path,  
                "filename": f"relatorio_validacao_{id_documento}.pdf"  
            }  
  
            contexto["analise"] = analise  
            contexto["report_id"] = report_id  
            contexto["sucesso"] = "Comparação realizada com sucesso."  
            contexto["json_texto"] = ""  
            contexto["id_documento_manual"] = ""  
  
        except FileNotFoundError as e:  
            contexto["erro"] = str(e)  
        except ValueError as e:  
            contexto["erro"] = str(e)  
        except Exception as e:  
            contexto["erro"] = f"Erro inesperado durante o processamento: {str(e)}"  
  
    return render_template("index.html", **contexto)  
  
  
@app.route("/download/pdf/<report_id>")  
def download_pdf(report_id):  
    report = REPORT_CACHE.get(report_id)  
  
    if not report:  
        return "Relatório não encontrado ou expirado.", 404  
  
    pdf_path = report["pdf_path"]  
    download_name = report["filename"]  
  
    if not os.path.exists(pdf_path):  
        return "Arquivo PDF não encontrado.", 404  
  
    return send_file(  
        pdf_path,  
        as_attachment=True,  
        download_name=download_name,  
        mimetype="application/pdf"  
    )  
  
  
if __name__ == "__main__":  
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)  