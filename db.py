import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    try: 
        if 'db' not in g:
            g.db = sqlite3.connect(current_app.config['DATABASE'],detect_types=sqlite3.PARSE_DECLTYPES)
            g.db.row_factory = sqlite3.Row
            print("Creating new database.")
    except:
        print("Database already created.")
    finally:
        return g.db

def close_db(e=None):
    try:
        db = g.pop('db', None)
        print("Database already shutdown.")
    except:
        if db is not None:
            db.close()
            print("Database shutdown.")

def init_db():
    db = get_db()
    try:
        with current_app.open_resources('schema.sql') as f:
            db.executescript(f.read().decode("utf8"))
            print("Database being read.")
    except sqlite3.OperationalError as err_num:
        print("Error reading database: err_num")

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)