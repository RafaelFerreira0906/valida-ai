import os  
import json  
import uuid  
import time  
from functools import wraps  
  
from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash  
from werkzeug.utils import secure_filename  
from werkzeug.security import generate_password_hash, check_password_hash  
  
from comparador import (  
    ALLOWED_EXTENSIONS,  
    detectar_tipo_documental,  
    obter_id_documento_do_arquivo,  
    localizar_gabarito,  
    analisar_comparacao_completa,  
    gerar_pdf_relatorio  
)  
  
app = Flask(__name__)  
app.secret_key = "troque_por_uma_chave_forte"  
  
app.config["SESSION_PERMANENT"] = False  
app.config["SESSION_COOKIE_HTTPONLY"] = True  
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  
app.config["SESSION_COOKIE_SECURE"] = False  
  
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
UPLOAD_FOLDER = os.path.join("/tmp", "uploads")  
REPORTS_FOLDER = os.path.join("/tmp", "reports")  
GABARITOS_DIR = os.path.join(BASE_DIR, "gabaritos")  
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")  
  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  
os.makedirs(REPORTS_FOLDER, exist_ok=True)  
  
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER  
app.config["REPORTS_FOLDER"] = REPORTS_FOLDER  
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  
  
REPORT_CACHE = {}  
  
  
def init_credentials():  
    if not os.path.exists(CREDENTIALS_FILE):  
        data = {  
            "users": [  
                {  
                    "username": "D004028",  
                    "password_hash": generate_password_hash("maylin031112")  
                },  
                {  
                    "username": "D004391",  
                    "password_hash": generate_password_hash("jessica123")  
                },  
                {  
                    "username": "D004433",  
                    "password_hash": generate_password_hash("samyra123")  
                }  
            ]  
        }  
        with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:  
            json.dump(data, f, indent=4)  
  
  
def load_credentials():  
    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:  
        return json.load(f)  
  
  
def find_user(username):  
    creds = load_credentials()  
    for user in creds.get("users", []):  
        if user["username"] == username:  
            return user  
    return None  
  
  
def update_user_credentials(current_username, new_username, new_password):  
    creds = load_credentials()  
  
    for user in creds.get("users", []):  
        if user["username"] == current_username:  
            user["username"] = new_username  
            user["password_hash"] = generate_password_hash(new_password)  
            break  
  
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:  
        json.dump(creds, f, indent=4)  
  
  
def login_required(func):  
    @wraps(func)  
    def wrapper(*args, **kwargs):  
        if not session.get("logged_in"):  
            flash("Faça login para acessar o sistema.", "error")  
            return redirect(url_for("login"))  
        return func(*args, **kwargs)  
    return wrapper  
  
  
@app.route("/login", methods=["GET", "POST"])  
def login():  
    if session.get("logged_in"):  
        return redirect(url_for("index"))  
  
    if request.method == "POST":  
        username = request.form.get("username", "").strip()  
        password = request.form.get("password", "").strip()  
  
        if not username or not password:  
            flash("Informe login e senha.", "error")  
            return render_template("login.html")  
  
        user = find_user(username)  
  
        if user and check_password_hash(user["password_hash"], password):  
            session.clear()  
            session.permanent = False  
            session["logged_in"] = True  
            session["username"] = username  
            return redirect(url_for("index"))  
        else:  
            flash("Login ou senha inválidos.", "error")  
  
    return render_template("login.html")  
  
  
@app.route("/logout")  
def logout():  
    session.clear()  
    flash("Logout realizado com sucesso.", "success")  
    return redirect(url_for("login"))  
  
  
@app.route("/force-logout")  
def force_logout():  
    session.clear()  
    return redirect(url_for("login"))  
  
  
@app.route("/alterar-credenciais", methods=["GET", "POST"])  
@login_required  
def alterar_credenciais():  
    if request.method == "POST":  
        current_username = request.form.get("current_username", "").strip()  
        new_username = request.form.get("new_username", "").strip()  
        current_password = request.form.get("current_password", "").strip()  
        new_password = request.form.get("new_password", "").strip()  
  
        if not current_username or not new_username or not current_password or not new_password:  
            flash("Preencha todos os campos.", "error")  
            return redirect(url_for("alterar_credenciais"))  
  
        user = find_user(current_username)  
  
        if not user:  
            flash("Login atual inválido.", "error")  
            return redirect(url_for("alterar_credenciais"))  
  
        if not check_password_hash(user["password_hash"], current_password):  
            flash("Senha atual inválida.", "error")  
            return redirect(url_for("alterar_credenciais"))  
  
        update_user_credentials(current_username, new_username, new_password)  
        session["username"] = new_username  
  
        flash("Credenciais alteradas com sucesso.", "success")  
        return redirect(url_for("index"))  
  
    return render_template("alterar_credenciais.html")  
  
  
@app.route("/", methods=["GET", "POST"])  
@login_required  
def index():  
    contexto = {  
        "erro": None,  
        "sucesso": None,  
        "analise": None,  
        "report_id": None,  
        "json_texto": "",  
        "id_documento_manual": "",  
        "username": session.get("username")  
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
        caminho_upload = None  
  
        try:  
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
@login_required  
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
    init_credentials()  
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)  