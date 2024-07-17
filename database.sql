CREATE TABLE urls (
    id serial primary key,
    name varchar(255) UNIQUE NOT NULL,
    created_at date DEFAULT CURRENT_DATE
);