from flask import g
import sqlite3

def connect_db():
    # Running on Local Server - Macbook
    # sql = sqlite3.connect('/Users/promieyutasane/Dropbox/Github/question-answer/qa.db')
    # Running on the local machine - windows
    sql = sqlite3.connect(r'C:\Users\pyutasane\Dropbox\Github\question-answer\qa.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db