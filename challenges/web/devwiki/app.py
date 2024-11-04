from flask import Flask, request, render_template_string, redirect, url_for, session
from flask_session import Session
import sqlite3
import os
from datetime import datetime, timedelta
import uuid
import shutil

app = Flask(__name__)

app.config.update(
    SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', os.urandom(24)),
    SESSION_TYPE='filesystem',
    SESSION_FILE_DIR='./sessions',
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),  # Sessions last 24 hours
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION=True  # Make sessions permanent
)
Session(app)

def get_user_db_path():
    """Get unique database path for current session"""
    if 'session_id' not in session:
        # Only generate new session_id if one doesn't exist
        session['session_id'] = str(uuid.uuid4())
        session.permanent = True  # Make the session persistent
    
    db_dir = f'./sessions/db/{session["session_id"]}'
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'wiki.db')

def init_db(db_path):
    """Initialize database only if it doesn't exist"""
    if os.path.exists(db_path):
        return
        
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS pages
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         content TEXT NOT NULL,
         template TEXT NOT NULL,
         last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')

    session_id_short = session['session_id'][:8]
    sample_pages = [
        (f'Welcome to DevDocs (Session {session_id_short})', 
         f'Welcome to your personal documentation space! This is a unique session ({session_id_short})', 
         'default'),
        (f'API Guidelines (Session {session_id_short})', 
         'Follow these best practices when developing APIs...', 
         'technical'),
        (f'Markdown Guide (Session {session_id_short})', 
         'Learn how to use our extended markdown syntax...', 
         'tutorial')
    ]
    c.executemany('INSERT INTO pages (title, content, template) VALUES (?, ?, ?)', sample_pages)
    conn.commit()
    conn.close()

def get_db():
    """Get database connection ensuring it's initialized"""
    db_path = get_user_db_path()
    if not os.path.exists(db_path):
        init_db(db_path)
    return sqlite3.connect(db_path)

def get_all_pages():
    conn = get_db()
    try:
        c = conn.cursor()
        c.execute('SELECT id, title FROM pages ORDER BY title')
        pages = c.fetchall()
        return pages
    finally:
        conn.close()

def get_page(page_id):
    conn = get_db()
    try:
        c = conn.cursor()
        c.execute('SELECT title, content, template, last_modified FROM pages WHERE id = ?', (page_id,))
        page = c.fetchone()
        return page
    finally:
        conn.close()

def cleanup_old_sessions():
    """Clean up old session databases"""
    sessions_dir = './sessions/db'
    if os.path.exists(sessions_dir):
        for session_id in os.listdir(sessions_dir):
            session_path = os.path.join(sessions_dir, session_id)
            if os.path.isdir(session_path):
                # Check if directory is older than 30 minutes
                modified_time = os.path.getmtime(session_path)
                if datetime.now().timestamp() - modified_time > 1800:  # 30 minutes
                    shutil.rmtree(session_path)

@app.before_request
def before_request():
    """Only initialize new sessions if one doesn't exist"""
    if 'session_id' not in session:
        session.permanent = True
        session['session_id'] = str(uuid.uuid4())
        init_db(get_user_db_path())

PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DevDocs - {{ title }}</title>
    <style>
        :root {
            --primary-color: #2563eb;
            --secondary-color: #1e40af;
            --text-color: #1f2937;
            --bg-color: #f3f4f6;
            --card-bg: #ffffff;
        }

        body {
            font-family: 'Inter', -apple-system, system-ui, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background: var(--bg-color);
            color: var(--text-color);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 30px;
        }

        .sidebar {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            height: fit-content;
        }

        .main-content {
            background: var(--card-bg);
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .header {
            background: var(--card-bg);
            padding: 20px;
            margin-bottom: 20px;
            border-bottom: 1px solid #e5e7eb;
        }

        .header h1 {
            margin: 0;
            color: var(--primary-color);
        }

        .nav-links {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .nav-links li {
            margin-bottom: 10px;
        }

        .nav-links a {
            color: var(--text-color);
            text-decoration: none;
            display: block;
            padding: 8px 12px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }

        .nav-links a:hover {
            background: var(--bg-color);
        }

        .page-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .button {
            background: var(--primary-color);
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            text-decoration: none;
            border: none;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.2s;
        }

        .button:hover {
            background: var(--secondary-color);
        }

        .search-box {
            padding: 8px;
            border: 1px solid #e5e7eb;
            border-radius: 4px;
            width: 100%;
            margin-bottom: 20px;
        }

        .metadata {
            font-size: 0.9em;
            color: #6b7280;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }

        .edit-form {
            display: grid;
            gap: 20px;
        }

        .form-group {
            display: grid;
            gap: 8px;
        }

        .form-group label {
            font-weight: 500;
        }

        .form-group input,
        .form-group textarea,
        .form-group select {
            padding: 8px;
            border: 1px solid #e5e7eb;
            border-radius: 4px;
            font-family: inherit;
        }

        .form-group textarea {
            min-height: 200px;
        }

        .alert {
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 20px;
        }

        .alert-success {
            background: #dcfce7;
            color: #166534;
        }

        .alert-error {
            background: #fee2e2;
            color: #991b1b;
        }

        .template-preview {
            background: #f8fafc;
            padding: 15px;
            border-radius: 4px;
            margin-top: 10px;
            border: 1px solid #e5e7eb;
        }

        code {
            font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
            background: #f1f5f9;
            padding: 2px 4px;
            border-radius: 4px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>DevDocs</h1>
    </div>
    
    <div class="container">
        <div class="sidebar">
            <input type="text" class="search-box" placeholder="Search documentation...">
            
            <nav>
                <ul class="nav-links">
                    {% for page in pages %}
                        <li><a href="/page/{{ page[0] }}">{{ page[1] }}</a></li>
                    {% endfor %}
                </ul>
            </nav>
            
            <div style="margin-top: 20px;">
                <a href="/new" class="button">Create New Page</a>
            </div>
        </div>

        <main class="main-content">
            {% if message %}
            <div class="alert {{ 'alert-success' if success else 'alert-error' }}">
                {{ message }}
            </div>
            {% endif %}

            {% if edit_mode %}
                <form class="edit-form" method="POST" action="{{ '/edit/' + page_id if page_id else '/new' }}">
                    <div class="form-group">
                        <label for="title">Title:</label>
                        <input type="text" id="title" name="title" value="{{ title }}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="content">Content:</label>
                        <textarea id="content" name="content" required>{{ content }}</textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="template">Template:</label>
                        <select id="template" name="template">
                            <option value="default" {% if template == 'default' %}selected{% endif %}>Default</option>
                            <option value="technical" {% if template == 'technical' %}selected{% endif %}>Technical</option>
                            <option value="tutorial" {% if template == 'tutorial' %}selected{% endif %}>Tutorial</option>
                            <option value="custom" {% if template == 'custom' %}selected{% endif %}>Custom</option>
                        </select>
                    </div>
                    
                    {% if template == 'custom' %}
                    <div class="form-group">
                        <label for="custom_template">Custom Template:</label>
                        <textarea id="custom_template" name="custom_template">{{ custom_template }}</textarea>
                        <div class="template-preview">
                            <small>Template variables: <code>{{ '{{ title }}' }}</code>, <code>{{ '{{ content }}' }}</code>, <code>{{ '{{ last_modified }}' }}</code></small>
                        </div>
                    </div>
                    {% endif %}
                    
                    <button type="submit" class="button">Save Page</button>
                </form>
            {% else %}
                <div class="page-controls">
                    <h2>{{ title }}</h2>
                    {% if page_id %}
                    <a href="/edit/{{ page_id }}" class="button">Edit Page</a>
                    {% endif %}
                </div>

                {% if template == 'custom' %}
                    {{ custom_content | safe }}
                {% else %}
                    {{ content | safe }}
                {% endif %}

                <div class="metadata">
                    Last modified: {{ last_modified }}
                    {% if template != 'default' %}
                    <br>
                    Template: {{ template }}
                    {% endif %}
                </div>
            {% endif %}
        </main>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    if request.args.get('new'):
        session.clear()
        return redirect(url_for('index'))
    
    pages = get_all_pages()
    session_id_short = session['session_id'][:8]
    return render_template_string(PAGE_TEMPLATE,
                                title=f"Welcome (Session {session_id_short})",
                                content=f"Select a page from the sidebar to begin. Your session ID: {session_id_short}",
                                pages=pages,
                                edit_mode=False)

@app.route('/page/<int:page_id>')
def view_page(page_id):
    pages = get_all_pages()
    page = get_page(page_id)
    
    if not page:
        return render_template_string(PAGE_TEMPLATE,
                                   title="Error",
                                   content="Page not found",
                                   pages=pages,
                                   edit_mode=False)
    
    title, content, template, last_modified = page
    
    if template == 'custom':
        try:
            custom_content = render_template_string(content,
                                                 title=title,
                                                 content=content,
                                                 last_modified=last_modified)
        except Exception as e:
            custom_content = f"Template Error: {str(e)}"
    else:
        custom_content = None
    
    return render_template_string(PAGE_TEMPLATE,
                               title=title,
                               content=content,
                               custom_content=custom_content,
                               template=template,
                               last_modified=last_modified,
                               pages=pages,
                               page_id=page_id,
                               edit_mode=False)

@app.route('/new', methods=['GET', 'POST'])
def new_page():
    pages = get_all_pages()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        template = request.form['template']

        conn = get_db()  # Use the session-specific database
        try:
            c = conn.cursor()
            c.execute('INSERT INTO pages (title, content, template) VALUES (?, ?, ?)',
                     (title, content, template))
            conn.commit()
        finally:
            conn.close()

        return redirect(url_for('index'))

    return render_template_string(PAGE_TEMPLATE,
                               title="New Page",
                               content="",
                               template="default",
                               pages=pages,
                               edit_mode=True)

@app.route('/edit/<int:page_id>', methods=['GET', 'POST'])
def edit_page(page_id):
    pages = get_all_pages()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        template = request.form['template']

        conn = get_db()
        try:
            c = conn.cursor()
            c.execute('UPDATE pages SET title = ?, content = ?, template = ?, last_modified = CURRENT_TIMESTAMP WHERE id = ?',
                     (title, content, template, page_id))
            conn.commit()
        finally:
            conn.close()

        return redirect(url_for('view_page', page_id=page_id))

    page = get_page(page_id)
    if not page:
        return redirect(url_for('index'))

    title, content, template, last_modified = page

    return render_template_string(PAGE_TEMPLATE,
                               title=title,
                               content=content,
                               template=template,
                               pages=pages,
                               page_id=page_id,
                               edit_mode=True)

@app.route('/new-session')
def new_session():
    """Force create a new session"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs('./sessions/db', exist_ok=True)
    app.run(host='0.0.0.0', port=8080)
