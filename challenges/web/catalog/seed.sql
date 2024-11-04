INSERT INTO books (title, author, price, genre, isbn) VALUES
    ('The Art of Computer Programming', 'Donald Knuth', 59.99, 'Computer Science', '978-0201896831'),
    ('Dune', 'Frank Herbert', 14.99, 'Science Fiction', '978-0441172719'),
    ('Pride and Prejudice', 'Jane Austen', 9.99, 'Classic', '978-0141439518'),
    ('The Hobbit', 'J.R.R. Tolkien', 12.99, 'Fantasy', '978-0547928227'),
    ('1984', 'George Orwell', 10.99, 'Dystopian', '978-0451524935'),
    ('Clean Code', 'Robert C. Martin', 44.99, 'Computer Science', '978-0132350884'),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 11.99, 'Classic', '978-0743273565'),
    ('Neuromancer', 'William Gibson', 13.99, 'Science Fiction', '978-0441569595'),
    ('Design Patterns', 'Gang of Four', 54.99, 'Computer Science', '978-0201633610'),
    ('Brave New World', 'Aldous Huxley', 12.99, 'Dystopian', '978-0060850524');

INSERT INTO secrets (key, value) VALUES 
    ('flag', 'cc_ctf{sql_injection_in_my_function}'),
    ('admin_note', 'Remember to sanitize inputs before deployment'),
    ('db_version', 'BookStore DB v3.1.4');
