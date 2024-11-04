from flask import Flask, request, render_template_string, send_file, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'documents'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

if not os.path.exists('db.json'):
    with open('db.json', 'w') as f:
        json.dump({
            "documents": [
                {
                    "id": "1",
                    "title": "Welcome Guide",
                    "filename": "welcome.pdf",
                    "category": "Onboarding",
                    "access_level": "Public"
                },
                {
                    "id": "2",
                    "title": "Security Policy",
                    "filename": "security_policy.pdf",
                    "category": "Policies",
                    "access_level": "Internal"
                }
            ]
        }, f)

PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Enterprise Document Manager</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .header h1 {
            margin: 0;
            color: #2d3748;
        }
        .search-bar {
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }
        .search-bar input {
            flex: 1;
            padding: 10px;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
        }
        .search-bar button {
            padding: 10px 20px;
            background: #4299e1;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .search-bar button:hover {
            background: #3182ce;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .card h3 {
            margin-top: 0;
            color: #2d3748;
        }
        .tag {
            display: inline-block;
            padding: 4px 8px;
            background: #ebf4ff;
            color: #4299e1;
            border-radius: 4px;
            font-size: 0.875rem;
            margin-right: 8px;
        }
        .document-list {
            margin-top: 20px;
        }
        .document-item {
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .document-info {
            flex: 1;
        }
        .document-actions {
            display: flex;
            gap: 10px;
        }
        .btn {
            padding: 8px 16px;
            border-radius: 4px;
            border: none;
            cursor: pointer;
            font-size: 0.875rem;
            text-decoration: none;
        }
        .btn-primary {
            background: #4299e1;
            color: white;
        }
        .btn-secondary {
            background: #edf2f7;
            color: #4a5568;
        }
        .btn:hover {
            opacity: 0.9;
        }
        .folder-path {
            background: #edf2f7;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
            font-family: monospace;
        }
        .alert {
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
        }
        .alert-success {
            background: #c6f6d5;
            color: #2f855a;
        }
        .alert-error {
            background: #fed7d7;
            color: #c53030;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Enterprise Document Manager</h1>
            <p>Secure document management for your organization</p>
        </div>

        {% if message %}
        <div class="alert {{ 'alert-success' if success else 'alert-error' }}">
            {{ message }}
        </div>
        {% endif %}

        <div class="card">
            <h3>Quick Access</h3>
            <div class="folder-path">
                Current Path: {{ current_path if current_path else 'Root' }}
            </div>
            <form action="/browse" method="get" class="search-bar">
                <input type="text" name="path" placeholder="Enter folder path to browse" value="{{ current_path }}">
                <button type="submit">Browse</button>
            </form>
        </div>

        <div class="document-list">
            {% for doc in documents %}
            <div class="document-item">
                <div class="document-info">
                    <h3>{{ doc.title }}</h3>
                    <span class="tag">{{ doc.category }}</span>
                    <span class="tag">{{ doc.access_level }}</span>
                </div>
                <div class="document-actions">
                    <a href="/view/{{ doc.filename }}" class="btn btn-primary">View Document</a>
                    <a href="/download/{{ doc.filename }}" class="btn btn-secondary">Download</a>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="grid">
            <div class="card">
                <h3>Security Features</h3>
                <ul>
                    <li>End-to-end encryption</li>
                    <li>Access control management</li>
                    <li>Audit logging</li>
                    <li>Secure file storage</li>
                </ul>
            </div>
            <div class="card">
                <h3>Quick Stats</h3>
                <ul>
                    <li>Total Documents: {{ documents|length }}</li>
                    <li>Storage Used: 128 MB</li>
                    <li>Active Users: 42</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
'''

def get_documents():
    with open('db.json', 'r') as f:
        data = json.load(f)
    return data['documents']

@app.route('/')
def index():
    documents = get_documents()
    return render_template_string(PAGE_TEMPLATE, documents=documents, current_path='/')

@app.route('/browse')
def browse():
    path = request.args.get('path', '/')
    documents = get_documents()
    
    try:
        files = os.listdir(path)
        return render_template_string(PAGE_TEMPLATE, 
                                   documents=documents, 
                                   current_path=path,
                                   message=f"Found {len(files)} items in directory",
                                   success=True)
    except Exception as e:
        return render_template_string(PAGE_TEMPLATE,
                                   documents=documents,
                                   current_path=path,
                                   message=f"Error accessing path: {str(e)}",
                                   success=False)

@app.route('/view/<path:filename>')
def view_file(filename):
    try:
        return send_file(filename)
    except Exception as e:
        return f"Error: {str(e)}", 404

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
