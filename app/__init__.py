from __future__ import print_function
from flask import Flask, render_template, g, request, session, redirect, url_for, abort, flash, jsonify
import os, sys
from flask_login import LoginManager, UserMixin
import sqlite3
from contextlib import closing
from werkzeug.debug import DebuggedApplication

app = Flask(__name__)
DATABASE=os.path.join(os.getcwd(), 'app/clinical.sqlite')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'somethingsecret'


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

def tables(db): 
    cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [str(r[0]) for  r in cursor.fetchall()]
    return tables

def columns(tables, db):
    columns = dict()
    for table_name in tables: 
        cursor = db.execute("PRAGMA table_info(" + table_name + ");")
        sub_cols = [(table_name + "." + str(row[1])) for row in cursor.fetchall()]
        columns[table_name] = sub_cols
    return columns

@app.route('/')
def index():
    db = connect_db()
    tabs = tables(db)
    cols = columns(tabs, db)
    return redirect(url_for('search'))

@app.route('/submitquery', methods=['GET', 'POST'])
def submitQuery(): 
    columns = request.form['columns']
    table1 = request.form['0']
    table2 = request.form['1']
    table3 = request.form['2']
    table4 = request.form['3']
    table5 = request.form['4']
    tabs = [table2, table3, table4, table5]
    #join = request.form['jointype']
    on = ""
    where = request.form['filter']
    group  = request.form['group']
    limit = request.form['limit']
    order = request.form['order']
    #v = {'columns': columns, 'table': table, 'join': join, 'join_table': join_table, 'col1': col1, 'col2': col2, 'where': where, 'order': order, 'limit': limit}
    if columns: 
        columns = "SELECT " + columns
    else: 
        flash("no columns specified")
    if table1:
        table1 = table1
    else:
        flash("no table specified")
    if not columns or not table1:
        return redirect(url_for('index'))
    if where:
        where = " WHERE " + where
    if group:
        group = " GROUP BY " + group
    if limit:
        limit = " LIMIT " + limit
    if order:
        order = " ORDER BY " + order
    for join_table in tabs: 
        if join_table:
            on = on + " " + " JOIN " + join_table + " ON " + table1 + ".user_id" + " = " + join_table + ".user_id"       
    q = columns + " FROM " + table1 + on + where + group + order + limit 
    print("\n\n", file = sys.stderr)
    print(q, file = sys.stderr)
    print("\n\n", file = sys.stderr)

    return redirect(url_for('querying', new_query = q))

@app.route('/querying')
def querying():
    db = connect_db()
    tabs = tables(db)
    cols = columns(tabs, db)
    try:
        cursor = db.execute(request.args.get('new_query'))
        data = [dict((cursor.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cursor.fetchall()]
        print("\n\n", file = sys.stderr)
        #print(data, file = sys.stderr)
        print("\n\n", file = sys.stderr)
        return render_template('search.html', tables = tabs, columns = cols, data = data)
    except: 
        flash('no data')
        return render_template('search.html', data = {"hi"}, tables = tabs, columns = cols)

@app.route('/search')
def search(): 
    db = connect_db()
    tabs = tables(db)
    cols = columns(tabs, db)
    return render_template('search.html', title = "HumanAPI", tables = tabs, columns = cols, data = {})

@app.route('/process', methods = ["POST", "GET"])
def process(): 
    q = str(request.json)
    print("\n\nhi: ", file = sys.stderr)
    print(q, file = sys.stderr)
    print("\n\n", file = sys.stderr)
    db = connect_db()
    tabs = tables(db)
    cols = columns(tabs, db)
    try:
        cursor = db.execute(q)
        data = [dict((cursor.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cursor.fetchall()]
        print("data:\n", file = sys.stderr)
        print("\n\n", file = sys.stderr)
        return jsonify(data)
    except: 
        flash('no data')
        return render_template('search.html', data = {"hi"}, tables = tabs, columns = cols)

@app.route('/test', methods = ["POST", "GET"])
def test():
    q = str(request.json)
    print("\n\n", file = sys.stderr)
    print(q, file = sys.stderr)
    print("\n\n", file = sys.stderr)
    db = connect_db()
    tabs = tables(db)
    cols = columns(tabs, db)
    try:
        cursor = db.execute(q)
        data = [dict((cursor.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cursor.fetchall()]
        print("data:\n", file = sys.stderr)
        print(data, file = sys.stderr)
        print("\n\n", file = sys.stderr)
        return jsonify(data)
        #return render_template('search.html', tables = tabs, columns = cols, data = data, hi = "hello there")
    except: 
        flash('no data')
        return render_template('query.html')


if __name__ == "__main__":
    application.run()


