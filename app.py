from flask import Flask, render_template, request, send_file, jsonify, session
import pandas as pd
import os
import time
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_segura'  # Necessária para usar sessões

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Define tempo de vida dos arquivos (em minutos)
SESSION_LIFETIME_MINUTES = 15

# Atribui um ID de sessão único se não existir
@app.before_request
def assign_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['created_at'] = time.time()

# Limpa arquivos antigos de sessões inativas
def clear_inactive_session_files(folder, session_lifetime_minutes=15):
    now = time.time()
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if now - file_mtime > session_lifetime_minutes * 60:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Erro ao remover {file_path}: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    clear_inactive_session_files(UPLOAD_FOLDER)
    clear_inactive_session_files(OUTPUT_FOLDER)

    file = request.files['excelFile']
    if not file:
        return "Nenhum arquivo enviado.", 400

    session_id = session.get('session_id')
    filename = f"{session_id}_{secure_filename(file.filename)}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    xls = pd.ExcelFile(path)
    return {'sheets': xls.sheet_names, 'filename': filename}

@app.route('/columns', methods=['POST'])
def get_columns():
    data = request.json
    path = os.path.join(UPLOAD_FOLDER, data['filename'])
    df = pd.read_excel(path, sheet_name=data['sheet'])
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_").str.replace(".", "")
    return {'columns': list(df.columns)}

@app.route('/generate', methods=['POST'])
def generate_sql():
    data = request.json
    filename = data['filename']
    sheet = data['sheet']
    template = data['template']
    output_name = data['output_name']

    if not output_name.lower().endswith('.sql'):
        output_name += '.sql'

    session_id = session.get('session_id')
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_filename = f"{session_id}_{secure_filename(output_name)}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    df = pd.read_excel(input_path, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_").str.replace(".", "")

    with open(output_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            try:
                sql = template.format(**row.to_dict())
                f.write(sql + "\n")
            except Exception:
                continue

    return {'download_url': f'/download/{output_filename}'}

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
