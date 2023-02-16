from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1365@192.168.86.245/mems'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('home.html', title = 'Home Page')


if __name__ == '__main__':
    app.run(debug=True)