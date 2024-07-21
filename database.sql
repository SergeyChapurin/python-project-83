CREATE TABLE IF NOT EXISTS urls (
    id serial primary key,
    name varchar(255) UNIQUE NOT NULL,
    created_at date DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS url_checks (
    id serial primary key,
    url_id int REFERENCES urls(id),
    status_code int,
    h1 varchar(255),
    title varchar(255),
    description varchar(255),
    created_at date DEFAULT CURRENT_DATE
);