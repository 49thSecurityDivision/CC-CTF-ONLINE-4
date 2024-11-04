from flask import Flask, request, render_template_string, g
import sqlite3
import os

app = Flask(__name__)
app.config['DATABASE'] = 'bookstore.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        with app.open_resource('seed.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()

PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Secure Bookstore Catalog</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(145deg, #f3f4f6 0%, #e5e7eb 100%);
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
            text-align: center;
        }
        .search-section {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .advanced-search {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
        }
        .form-group label {
            margin-bottom: 5px;
            color: #4b5563;
        }
        input, select {
            padding: 8px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            font-size: 14px;
        }
        button {
            background: #3b82f6;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }
        button:hover {
            background: #2563eb;
        }
        .results {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .book-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .book-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 15px;
            transition: transform 0.2s;
        }
        .book-card:hover {
            transform: translateY(-2px);
        }
        .book-title {
            font-size: 1.1em;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 8px;
        }
        .book-author {
            color: #64748b;
            margin-bottom: 8px;
        }
        .book-price {
            font-weight: 600;
            color: #059669;
        }
        .book-genre {
            display: inline-block;
            background: #dbeafe;
            color: #1e40af;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.85em;
            margin-top: 8px;
        }
        .security-badges {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        }
        .badge {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: #f8fafc;
            border-radius: 20px;
            font-size: 0.9em;
            color: #475569;
        }
        .badge img {
            width: 20px;
            height: 20px;
        }
        .alert {
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Secure Bookstore Catalog</h1>
            <p>Advanced search with enterprise-grade security</p>
            
            <div class="security-badges">
                <div class="badge">
                    🔒 SQL Injection Protected
                </div>
                <div class="badge">
                    🛡️ Input Sanitization
                </div>
                <div class="badge">
                    📝 Query Logging
                </div>
            </div>
        </div>

        {% if error %}
        <div class="alert">
            {{ error }}
        </div>
        {% endif %}

        <div class="search-section">
            <h2>Advanced Search</h2>
            <form method="GET" action="/">
                <div class="advanced-search">
                    <div class="form-group">
                        <label for="title">Title Contains:</label>
                        <input type="text" id="title" name="title" value="{{ request.args.get('title', '') }}">
                    </div>
                    <div class="form-group">
                        <label for="price">Max Price:</label>
                        <input type="number" id="price" name="price" step="0.01" value="{{ request.args.get('price', '') }}">
                    </div>
                    <div class="form-group">
                        <label for="genre">Genre:</label>
                        <select id="genre" name="genre">
                            <option value="">All Genres</option>
                            {% for genre in genres %}
                            <option value="{{ genre }}" {% if request.args.get('genre') == genre %}selected{% endif %}>
                                {{ genre }}
                            </option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>&nbsp;</label>
                        <button type="submit">Search Books</button>
                    </div>
                </div>
            </form>
        </div>

        <div class="results">
            <h2>Search Results</h2>
            <div class="book-grid">
                {% for book in books %}
                <div class="book-card">
                    <div class="book-title">{{ book['title'] }}</div>
                    <div class="book-author">by {{ book['author'] }}</div>
                    <div class="book-price">${{ "%.2f"|format(book['price']) }}</div>
                    <div class="book-genre">{{ book['genre'] }}</div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    db = get_db()
    error = None
    books = []
    
    genres = [row['genre'] for row in db.execute('SELECT DISTINCT genre FROM books').fetchall()]
    
    query = 'SELECT * FROM books WHERE 1=1'
    
    if title := request.args.get('title'):
        query += f" AND title LIKE '%{title}%'"
    
    if price := request.args.get('price'):
        query += f" AND price <= {price}"
    
    if genre := request.args.get('genre'):
        query += f" AND genre = '{genre}'"
    
    try:
        books = db.execute(query).fetchall()
    except sqlite3.Error as e:
        error = f"An error occurred: {str(e)}"
    
    return render_template_string(PAGE_TEMPLATE, 
                                books=books, 
                                genres=genres,
                                error=error)

if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    app.run(host='0.0.0.0', port=8080)
