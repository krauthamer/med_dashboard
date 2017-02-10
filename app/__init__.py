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

#TODO! NEED TO SET UP SQL ALCHEMY AND MODEL FILE!!!!

@app.route('/')
def instructions(): 
    return render_template('instructions.html', title = "Instructions")

@app.route('/test_entry')
def tentry(): 
    types = get_test_types()
    return render_template('test_data_entry.html', types = types, title = "Input Test Options", active_tests = "active")

@app.route('/view_tests')
def view_tests(): 
    return render_template('view_entered_tests.html', active_view = "active")

# @app.route('/remedy_entry')
# def rentry(): 
#     return render_template('remedies_data_entry.html', title = "Input Available Remedies")

@app.route('/dosage_entry')
def dosentry(): 
    return render_template('dosage_data_entry.html', title = "Input Dosage Options", active_dosage = "active")

# @app.route('/input')
# def input(): 
#     return render_template('input_patient_data.html', title = "Input Patient Data")

@app.route('/add_test', methods = ["POST", "GET"])
def enterTest(): 
    values = str(request.json)
    values = values.rsplit(":::")
    name = values[0].strip()
    meaning = values[1].strip()
    actual_ampules = values[2].strip()
    code_name = values[3].strip()
    test_type = values[4].strip()
    result = insert_test(name, meaning, actual_ampules, code_name, test_type)
    return jsonify(result)

@app.route('/add_dosage', methods = ["POST", "GET"])
def enterDosage(): 
    values = str(request.json)
    values = values.rsplit(':::')
    #print(values)
    number = values[0].strip()
    unit = values[1].strip()
    insert_dosages(number, unit)
    data = retrieve_dosages()
    #print(data)
    return jsonify(data)

def get_test_types():
    db = connect_db()
    try:
        cursor = db.execute("SELECT * from testType;")
        types = [(str(r[0]), str(r[0]).replace('_', ' ').title()) for  r in cursor.fetchall()]
        types.sort()
        return types
    except: 
        flash('problem retrieving test types from the database')

def insert_test(name, meaning, actual_ampules, code_name, test_type):
    db = connect_db()
    sql = 'INSERT INTO tests (name, meaning, actual_ampules, code_name, type) VALUES (?, ?, ?, ?, ?)'
    db.executemany(sql, [(name, meaning, actual_ampules, code_name, test_type)])
    db.commit()
    return "success"

def retrieve_dosages():
    db = connect_db()
    try:
        sql = "SELECT * FROM dosage_enum"
        cursor = db.execute(sql)
        data = [dict((cursor.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cursor.fetchall()]
        return data
    except: 
        flash('no data')
        return redirect(url_for('/'))


def insert_dosages(number, unit):
    db = connect_db()
    sql = 'INSERT INTO dosage_enum (dosage, unit) VALUES (?, ?)'
    db.executemany(sql, [(number, unit)])
    db.commit()
    return "success"

@app.route('/retrieveQueryResults', methods = ["POST", "GET"])
def process(): 
    query = str(request.json)
    print("\nSubmitted query:\n", file = sys.stderr)
    print(query, file = sys.stderr)
    print("\n", file = sys.stderr)
    db = connect_db()
    try:
        cursor = db.execute(query)
        data = [dict((cursor.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cursor.fetchall()]
        print("First data point:\n", file = sys.stderr)
        print(data[0], file = sys.stderr)
        print("\n", file = sys.stderr)
        return jsonify(data)
    except: 
        flash('no data')
        return redirect(url_for('instructions'))

@app.route('/delete_entry', methods = ["POST", "GET"])
def delete_entry():
    db = connect_db()
    sql = str(request.json)
    print("\nSubmitted query:\n", file = sys.stderr)
    print(sql, file = sys.stderr)
    print("\n", file = sys.stderr)
    db.execute(sql)
    db.commit()
    return jsonify("successfully deleted entry")

# def data_viz_data(query):
#     db = connect_db()
#     try:
#         cursor = db.execute(query)
#         col_names = ['label', 'value']
#         data = []
#         for row in cursor.fetchall():
#             data.append({col_names[0]: str(row[0]), col_names[1]: row[1]})
#         print(data, file = sys.stderr)
#         return data
#     except:
#         flash("I don't understand")
#         return data


# def tables(db): 
#     cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = [str(r[0]) for  r in cursor.fetchall()]
#     return tables
# 
# def columns(tables, db):
#     columns = dict()
#     for table_name in tables: 
#         cursor = db.execute("PRAGMA table_info(" + table_name + ");")
#         sub_cols = [[(table_name + "." + str(row[1])) , string.capwords(str(row[1]).replace('_', ' '))] for row in cursor.fetchall()]
#         columns[table_name] = sub_cols
#         print(columns, file = sys.stderr)
#     return columns
# 
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





# @app.route('/testing', methods = ["POST", "GET"])
# def testing(): 
#     q = str(request.json)
#     #print(q, file = sys.stderr)
#     #print("\n", file = sys.stderr)
#     db = connect_db()
#     try:
#         cursor = db.execute(q)
#         data = [dict((cursor.description[idx][0], value) for idx, value in enumerate(row)) for row in cursor.fetchall()]
#         #print(data, file = sys.stderr)
#         return jsonify(data)
#     except: 
#         flash('no data')
#         return redirect(url_for('test'))
# 
# @app.route('/search')
# def index():
#     return redirect(url_for('search'))
# 
# @app.route('/graphs')
# def graphs():
#     q = "select * from counts;"
#     data = data_viz_data(q)
#     return render_template('data_visualizations.html', data = data)

