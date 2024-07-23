from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    abort
)
from dotenv import load_dotenv
import os
from datetime import datetime
import requests
from page_analyzer.utils import validate, normalize, parse_url
from page_analyzer.db import (
    get_db_connection,
    get_url_by_name,
    insert_url,
    get_url_by_id,
    get_url_checks,
    get_all_urls,
    add_url_check
)


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


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
    existing_url = get_url_by_name(conn, url)

    if existing_url:
        flash('Страница уже существует', 'info')
        url_id = existing_url.id
    else:
        url_id = insert_url(conn, url).id
        conn.commit()
        flash('Страница успешно добавлена', 'success')

    conn.close()
    return redirect(url_for('show_url', id=url_id))


@app.route('/urls/<int:id>')
def show_url(id):
    conn = get_db_connection()
    url = get_url_by_id(conn, id)

    if url is None:
        conn.close()
        abort(404)

    checks = get_url_checks(conn, id)
    conn.close()
    return render_template('url.html', url=url, checks=checks)


@app.route('/urls')
def show_urls():
    conn = get_db_connection()
    urls = get_all_urls(conn)
    conn.close()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def add_check(id):
    conn = get_db_connection()
    url = get_url_by_id(conn, id)

    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        conn.close()
        return redirect(url_for('show_url', id=id))

    status_code, h1, title, description = parse_url(response)
    created_at = datetime.now()
    add_url_check(conn, id, status_code, h1, title, description, created_at)
    conn.close()
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url', id=id))


@app.errorhandler(404)
def url_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
