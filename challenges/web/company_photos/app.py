from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for, session
from flask_session import Session
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import timedelta
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

app.config.update(
    SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', os.urandom(24)),
    SESSION_TYPE='filesystem',
    SESSION_FILE_DIR='./sessions',
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION=True
)
Session(app)

def get_user_upload_folder():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session.permanent = True

    upload_dir = f'uploads/{session["session_id"]}'
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir

@app.before_request
def before_request():
    """Initialize session if needed"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session.permanent = True
        # Create user-specific upload directory and copy default image
        upload_dir = get_user_upload_folder()

PAGE_TEMPLATE = '''
<!DeCTYPE html>
<html>
<head>
    <title>Employee Profile Portal</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .profile-section {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }
        .profile-image {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #fff;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .profile-info {
            flex: 1;
        }
        .upload-form {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .input-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #4a5568;
        }
        input[type="text"],
        input[type="email"],
        input[type="file"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        button {
            background: #4299e1;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s ease;
        }
        button:hover {
            background: #3182ce;
        }
        .alert {
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        .alert-success {
            background-color: #c6f6d5;
            color: #2f855a;
        }
        .alert-error {
            background-color: #fed7d7;
            color: #c53030;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .feature-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .feature-icon {
            font-size: 24px;
            margin-bottom: 10px;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .gallery img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 4px;
            transition: transform 0.3s ease;
        }
        .gallery img:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>Employee Profile Portal</h1>
            
            <div class="profile-section">
                <img src="/uploads/default.jpg" alt="Profile Picture" class="profile-image">
                <div class="profile-info">
                    <h2>Update Your Profile</h2>
                    <p>Welcome to the secure employee profile management system. Upload your profile picture and update your information below.</p>
                </div>
            </div>

            {% if message %}
            <div class="alert {{ 'alert-success' if success else 'alert-error' }}">
                {{ message }}
            </div>
            {% endif %}

            <div class="upload-form">
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <div class="input-group">
                        <label for="name">Full Name:</label>
                        <input type="text" id="name" name="name" required>
                    </div>

                    <div class="input-group">
                        <label for="email">Corporate Email:</label>
                        <input type="email" id="email" name="email" required>
                    </div>

                    <div class="input-group">
                        <label for="photo">Profile Photo:</label>
                        <input type="file" id="photo" name="photo" accept="image/*" required>
                        <small>Supported formats: JPG, PNG, GIF (Max size: 16MB)</small>
                    </div>

                    <button type="submit">Update Profile</button>
                </form>
            </div>
        </div>

        <div class="features">
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3>Secure Storage</h3>
                <p>All files are stored with enterprise-grade security</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Fast Upload</h3>
                <p>Optimized for quick file processing</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <h3>Mobile Ready</h3>
                <p>Access your profile from any device</p>
            </div>
        </div>

        {% if uploaded_files %}
        <div class="card">
            <h2>Recent Uploads</h2>
            <div class="gallery">
                {% for file in uploaded_files %}
                <img src="/uploads/{{ file }}" alt="Uploaded file">
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

def get_uploaded_files():
    """Get files for current session"""
    upload_dir = get_user_upload_folder()
    files = []
    if os.path.exists(upload_dir):
        for file in os.listdir(upload_dir):
            if os.path.isfile(os.path.join(upload_dir, file)):
                files.append(file)
    return files

@app.route('/')
def index():
    uploaded_files = get_uploaded_files()
    session_id = session.get('session_id', '')[:8]  # Show part of session ID
    return render_template_string(
        PAGE_TEMPLATE, 
        uploaded_files=uploaded_files,
        session_id=session_id
    )

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Vulnerable file handler that executes certain files"""
    full_path = os.path.join(get_user_upload_folder(), filename)
    
    if filename.endswith(('.py', '.sh', '.pl')):
        try:
            os.chmod(full_path, 0o755)
            output = subprocess.check_output([full_path], stderr=subprocess.STDOUT, timeout=5)
            return output.decode(), 200, {'Content-Type': 'text/plain'}
        except Exception as e:
            return str(e), 500
    
    return send_from_directory(get_user_upload_folder(), filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        return render_template_string(PAGE_TEMPLATE,
                                   message='No file selected',
                                   success=False)

    file = request.files['photo']
    if file.filename == '':
        return render_template_string(PAGE_TEMPLATE,
                                   message='No file selected',
                                   success=False)

    filename = secure_filename(file.filename)
    upload_folder = get_user_upload_folder()
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    
    try:
        os.chmod(file_path, 0o755)
    except Exception:
        pass

    return render_template_string(
        PAGE_TEMPLATE,
        message=f'File {filename} uploaded successfully!',
        success=True
    )

@app.route('/new-session')
def new_session():
    """Force create a new session"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('./sessions', exist_ok=True)
    app.run(host='0.0.0.0', port=8080)
