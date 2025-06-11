from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['excelFile']
    if not file:
        return "Nenhum arquivo enviado.", 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    xls = pd.ExcelFile(path)
    return {'sheets': xls.sheet_names, 'filename': filename}

@app.route('/columns', methods=['POST'])
def get_columns():
    data = request.json
    path = os.path.join(UPLOAD_FOLDER, data['filename'])
    df = pd.read_excel(path, sheet_name=data['sheet'])

    # Limpa e padroniza os nomes das colunas
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

    path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    df = pd.read_excel(path, sheet_name=sheet)

    # Limpa e padroniza os nomes das colunas
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_").str.replace(".", "")

    with open(output_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            try:
                sql = template.format(**row.to_dict())
                f.write(sql + "\n")
            except Exception as e:
                continue

    return {'download_url': f'/download/{output_name}'}

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
