from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages)
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
import validators
from urllib.parse import urlparse
from datetime import datetime


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def validate(url):
    errors = []
    if not validators.url(url):
        errors.append('Некорректный URL')
    elif len(url) > 255:
        errors.append('URL превышает 255 символов')
    return errors


def normalize(url):
    normalized_url = urlparse(url)
    return f"{normalized_url.scheme}://{normalized_url.netloc}"


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    url = request.form.get('url')
    errors = validate(url)

    if errors:
        for error in errors:
            flash(error, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', url=url, messages=messages), 422

    url = normalize(url)
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute('SELECT * FROM urls WHERE name = %s', (url,))
    existing_url = cur.fetchone()

    if existing_url:
        flash('Страница уже существует', 'info')
        url_id = existing_url.id
    else:
        cur.execute(
            'INSERT INTO urls (name) VALUES (%s) RETURNING id',
            (url,)
        )
        url_id = cur.fetchone().id
        conn.commit()
        flash('Страница успешно добавлена', 'success')

    cur.close()
    conn.close()
    return redirect(url_for('show_url', id=url_id))


@app.route('/urls/<int:id>')
def show_url(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute(
        'SELECT id, name, created_at FROM urls WHERE id = %s',
        (id,)
    )
    url = cur.fetchone()
    if url is None:
        return render_template('error/404.html'), 404
    cur.execute(
        'SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC',
        (id,)
    )
    checks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('url.html', url=url, checks=checks)


@app.route('/urls')
def show_urls():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute(
        'SELECT urls.id, urls.name, MAX(url_checks.created_at) AS last_check '
        'FROM urls '
        'LEFT JOIN url_checks ON urls.id = url_checks.url_id '
        'GROUP BY urls.id '
        'ORDER BY urls.id DESC'
    )
    urls = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def add_check(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    created_at = datetime.now()
    cur.execute(
        'INSERT INTO url_checks (url_id, created_at) VALUES (%s, %s)',
        (id, created_at)
    )
    conn.commit()
    cur.close()
    conn.close()
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url', id=id, created_at=created_at))


if __name__ == '__main__':
    app.run(debug=True)
