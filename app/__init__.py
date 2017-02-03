from __future__ import print_function
from flask import Flask, render_template, g, request, session, redirect, url_for, abort, flash, jsonify
import os, sys, string
from flask_login import LoginManager, UserMixin
import sqlite3
from contextlib import closing
from werkzeug.debug import DebuggedApplication

app = Flask(__name__, static_folder='static', static_url_path='/static')
DATABASE=os.path.join(os.getcwd(), 'app/clinical.sqlite')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'somethingsecret'

@app.route('/')
def search(): 
    db = connect_db()
    tabs = tables(db)
    cols = columns(tabs, db)
    #print("\ntables:\n", file = sys.stderr)
    #print(tabs, file = sys.stderr)
    return render_template('search.html', title = "Demo", tables = tabs, columns = cols, data = {})

@app.route('/data_entry')
def dentry(): 
    db = connect_db()
    try:
        cursor = db.execute("SELECT * from testType;")
        types = [str(r[0]) for  r in cursor.fetchall()]
    except: 
        flash('problem retrieving test types from the database')
    return render_template('data_entry.html', types = types)

@app.route('/input')
def input(): 
    return render_template('input_patient_data.html')


@app.route('/retrieveQueryResults', methods = ["POST", "GET"])
def process(): 
    q = str(request.json)
    print("\nSubmitted query:\n", file = sys.stderr)
    print(q, file = sys.stderr)
    print("\n", file = sys.stderr)
    db = connect_db()
    try:
        cursor = db.execute(q)
        data = [dict((cursor.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cursor.fetchall()]
        print("First data point:\n", file = sys.stderr)
        print(data[0], file = sys.stderr)
        print("\n", file = sys.stderr)
        return jsonify(data)
    except: 
        flash('no data')
        return redirect(url_for('/'))

@app.route('/specificQueries')
def test():
    #db = connect_db()
    #cursor = db.execute("SELECT * FROM counts_of_users_with_x;")
    #counts = [ [str(row[0]), str(row[1]), str(row[2]) + ": " + str(row[1])] for row in cursor.fetchall()]
    #[dict((cursor.description[idx][0], value) for idx, value in enumerate(row)) for row in cursor.fetchall()]

    return render_template('specific_queries.html')#, counts = counts)

@app.route('/testing', methods = ["POST", "GET"])
def testing(): 
    q = str(request.json)
    #print(q, file = sys.stderr)
    #print("\n", file = sys.stderr)
    db = connect_db()
    try:
        cursor = db.execute(q)
        data = [dict((cursor.description[idx][0], value) for idx, value in enumerate(row)) for row in cursor.fetchall()]
        #print(data, file = sys.stderr)
        return jsonify(data)
    except: 
        flash('no data')
        return redirect(url_for('test'))

@app.route('/search')
def index():
    return redirect(url_for('search'))

@app.route('/graphs')
def graphs():
    q = "select * from counts;"
    data = data_viz_data(q)
    return render_template('data_visualizations.html', data = data)

def data_viz_data(query):
    db = connect_db()
    try:
        cursor = db.execute(query)
        col_names = ['label', 'value']
        data = []
        for row in cursor.fetchall():
            data.append({col_names[0]: str(row[0]), col_names[1]: row[1]})
        print(data, file = sys.stderr)
        return data
    except:
        flash("I don't understand")
        return data


def tables(db): 
    cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [str(r[0]) for  r in cursor.fetchall()]
    return tables

def columns(tables, db):
    columns = dict()
    for table_name in tables: 
        cursor = db.execute("PRAGMA table_info(" + table_name + ");")
        sub_cols = [[(table_name + "." + str(row[1])) , string.capwords(str(row[1]).replace('_', ' '))] for row in cursor.fetchall()]
        columns[table_name] = sub_cols
        print(columns, file = sys.stderr)
    return columns

def connect_db():
    try: 
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db
    except:
        print("couldn't connect")

def before_request():
    try:
        g.db = connect_db()
    except:
        print('exception')

@app.teardown_appcontext
def close_connection(exception):
    try:
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
    except:
        print('exception')

if __name__ == "__main__":
    application.run()


