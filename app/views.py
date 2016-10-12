from flask import render_template
from app import app

@app.route('/')
def index():
    cursor = db.execute('SELECT user_id, allergy_name FROM allergies LIMIT 10')
    data = [dict(user=row[0], allergy=row[1]) for row in cursor.fetchall()]
    return render_template('data.html', data = data)