import mysql.connector
import mysql.connector.errors as err
from flask import g

def get_db():
    if 'db' not in g:
        try:
            # Defaulting to root/root as per CLI app's default suggestion
            # In a real app, use env vars.
            g.db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="root",
                database="library"
            )
        except err.ProgrammingError:
            # Fallback or error handling
            print("Database connection failed. Check credentials.")
            return None
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
