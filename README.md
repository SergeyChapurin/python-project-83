# Page Analyzer
***

__Page Analyzer__ - analyzes the specified URLs for SEO suitability.


### Hexlet tests and linter status:
[![Actions Status](https://github.com/SergeyChapurin/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/SergeyChapurin/python-project-83/actions)
[![Python CI](https://github.com/SergeyChapurin/python-project-83/actions/workflows/python_CI.yml/badge.svg)](https://github.com/SergeyChapurin/python-project-83/actions/workflows/python_CI.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/c7468eecd76dacb5e9fc/maintainability)](https://codeclimate.com/github/SergeyChapurin/python-project-83/maintainability)

## Stack

To install and use an application you should have:
- python = "^3.10"
- flask = "^3.0.3"
- python-dotenv = "^1.0.1"
- gunicorn = "^22.0.0"
- psycopg2-binary = "^2.9.9"
- validators = "^0.33.0"
- requests = "^2.32.3"
- bs4 = "^0.0.2"
- flake8 = "^7.1.0"

The project also uses PostgreSQL as a relational database management system.


## Installation

1. Clone the project repository to your local device:
```
git clone git@github.com:SergeyChapurin/python-project-83.git
```
2. Change to the project directory:
```
cd python-project-83
```
3. Install the necessary dependencies using Poetry:
```
make install
```
4. Create a .env file to store your confidential settings:

```
cp .env.example .env
```

Open the .env file and replace the values for SECRET_KEY and DATABASE_URL.

5. Execute the commands from database.sql in your database's SQL console to create the required tables.

***

## Usage
1. To start the Flask server using Gunicorn, run the command:

```
make start
```
By default, the server will be available at http://0.0.0.0:8000.

2. You can also start the server locally in development mode with the debugger enabled:

```
make dev
```
The development server will be available at http://127.0.0.1:5000.

To add a new site, enter its address in the form on the home page. The entered address will be validated and added to the database.

After adding a site, you can start a check for it. On the page of each specific site, a button will appear. By clicking it, you will create a record in the checks table.

All added URLs can be viewed on the /urls page.

***
## Usage Modes
The project can be used both locally and online (e.g., with a third-party service like [render.com](https://dashboard.render.com/)).

***
## Demonstration
A demonstration of the project is available at the [provided link](https://python-project-83-ay3t.onrender.com/).
***