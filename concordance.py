from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def frontpage():
    return render_template('base.html')

