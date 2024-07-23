from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def get_url_by_name(conn, url):
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute(
        '''
        SELECT *
        FROM urls
        WHERE name = %s
        ''',
        (url,)
    )
    result = cur.fetchone()
    cur.close()
    return result


def insert_url(conn, url):
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute(
        '''
        INSERT INTO urls (name)
        VALUES (%s)
        RETURNING id
        ''',
        (url,)
    )
    result = cur.fetchone()
    cur.close()
    return result


def get_url_by_id(conn, id):
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute(
        '''
        SELECT id, name, created_at
        FROM urls
        WHERE id = %s
        ''',
        (id,)
    )
    result = cur.fetchone()
    cur.close()
    return result


def get_url_checks(conn, id):
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute(
        '''
        SELECT *
        FROM url_checks
        WHERE url_id = %s
        ORDER BY id DESC
        ''',
        (id,)
    )
    result = cur.fetchall()
    cur.close()
    return result


def get_all_urls(conn):
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute(
        '''
        SELECT DISTINCT ON (urls.id)
            urls.id,
            urls.name,
            MAX(url_checks.created_at) AS last_check,
            url_checks.status_code
        FROM urls
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
        GROUP BY urls.id, urls.name, url_checks.status_code
        ORDER BY urls.id DESC
        '''
    )
    result = cur.fetchall()
    cur.close()
    return result


def add_url_check(conn, id, status_code, h1, title, description, created_at):
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute(
        '''
        INSERT INTO url_checks (
            url_id,
            status_code,
            h1,
            title,
            description,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ''',
        (id, status_code, h1, title, description, created_at)
    )
    conn.commit()
    cur.close()
