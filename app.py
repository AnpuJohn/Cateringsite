from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from send_mail import send_mail
app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/catering'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Catering(db.Model):
    _tablename_ = 'catering'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    number = db.Column(db.Integer)
    date = db.Column(DateTime, default=datetime.datetime.utcnow)
    message = db.Column(db.Text())

    def __init__(self, name, number, date, message):
        self.name = name
        self.number = number
        self.date = date
        self.message = message


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        date = request.form['date']
        message = request.form['message']
        print(name, number, date, message)

        if db.session.query(Catering).filter(Catering.name == name).count() == 0:
            data = Catering(name, number, date, message)
            db.session.add(data)
            db.session.commit()
            send_mail(name, number, date, message)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == 'main':
    app.debug = True
    app.run()
