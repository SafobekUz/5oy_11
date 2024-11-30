import psycopg2
from datetime import datetime, timedelta

conn = psycopg2.connect(
    database='autosalon',
    user='postgres',
    host='localhost',
    password='1'
)
cursor = conn.cursor()

#1
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS news (
    id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(id),
    title VARCHAR(200) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_published BOOLEAN DEFAULT FALSE,
    views INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    news_id INT REFERENCES news(id),
    author_name TEXT,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

#2
categories = [
    ('Technology', 'All about technology'),
    ('Sports', 'Sports news and updates'),
    ('Health', 'Health and wellness tips')
]
cursor.executemany("INSERT INTO categories (name, description) VALUES (%s, %s)", categories)

news = [
    (1, 'Tech Revolution', 'Technology is evolving rapidly.', False),
    (2, 'Football Finals', 'The finals were exhilarating.', False),
    (3, 'Health Tips', 'Stay hydrated for better health.', True)
]
cursor.executemany("""
INSERT INTO news (category_id, title, content, is_published) 
VALUES (%s, %s, %s, %s)
""", news)

comments = [
    (1, 'Ali', 'Amazing update on technology!'),
    (2, 'Sara', 'Great sports news.'),
    (3, 'John', 'Helpful health tips.')
]
cursor.executemany("""
INSERT INTO comments (news_id, author_name, comment_text) 
VALUES (%s, %s, %s)
""", comments)

#3
cursor.execute("UPDATE news SET views = views + 1")
cursor.execute("""
UPDATE news SET is_published = TRUE 
WHERE published_at < (CURRENT_TIMESTAMP - INTERVAL '1 day')
""")

#4
cursor.execute("""
DELETE FROM comments 
WHERE created_at < (CURRENT_TIMESTAMP - INTERVAL '1 year')
""")

#5
cursor.execute("""
SELECT n.id AS news_id, n.title AS news_title, c.name AS category_name 
FROM news n 
JOIN categories c ON n.category_id = c.id
""")
print("News with categories:")
print(cursor.fetchall())

cursor.execute("""
SELECT * FROM news 
WHERE category_id = (SELECT id FROM categories WHERE name = 'Technology')
""")
print("Technology news:")
print(cursor.fetchall())

cursor.execute("""
SELECT * FROM news 
WHERE is_published = TRUE 
ORDER BY published_at DESC 
LIMIT 5
""")
print("Top 5 published news:")
print(cursor.fetchall())

cursor.execute("""
SELECT * FROM news 
WHERE views BETWEEN 10 AND 100
""")
print("News with views between 10 and 100:")
print(cursor.fetchall())

cursor.execute("""
SELECT * FROM comments 
WHERE author_name LIKE 'A%'
""")
print("Comments with author name starting with 'A':")
print(cursor.fetchall())

cursor.execute("""
SELECT * FROM comments 
WHERE author_name IS NULL
""")
print("Comments with null author name:")
print(cursor.fetchall())

cursor.execute("""
SELECT c.name AS category_name, COUNT(n.id) AS news_count 
FROM categories c 
LEFT JOIN news n ON c.id = n.category_id 
GROUP BY c.name
""")
print("News count by category:")
print(cursor.fetchall())

conn.commit()
cursor.close()
conn.close()
