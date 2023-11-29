from db_models import app
from flask import render_template
from datetime import datetime

@app.route("/")
def index():
    return render_template('index.html', date=datetime.now().strftime("%d %B %Y"))

@app.route("/add")
def add():
    return render_template('add.html')

@app.route("/connect")
def connect():
    return render_template('connect.html')
