from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "abcd"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///event_database.db"
db = SQLAlchemy(app)

class User(db.Model):
    #id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, primary_key = True)
    password = db.Column(db.String(100), nullable = False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sender_email = db.Column(db.String(100), nullable = False)
    receiver_email = db.Column(db.String(100), nullable = False)
    entry = db.Column(db.String(500),nullable = False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    icode = db.Column(db.Integer, nullable = False)
    ename = db.Column(db.String(100), nullable = False)
    edesc = db.Column(db.String(500), nullable = True)
    eadmin = db.Column(db.String(500), nullable = False)

class EventSec(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    icode = db.Column(db.Integer, nullable = False)
    ename = db.Column(db.String(100), nullable = False)
    member_email = db.Column(db.String(100),nullable = False)
    
db.create_all()

@app.route("/",methods=["POST","GET"])
def dashboard():
    if "email" in session:
        email = session["email"]
        user_name = User.query.filter_by(email = email).first().username
        #_notifications = Notification.query.filter_by(email = email).all()
        return render_template("dashboard.html",user_name = user_name) #notifications = _notifications)
    else:
        return redirect("/login/")
    #return redirect("/login/")

@app.route("/logout/")
def logout():
    session.pop("email",None)
    return redirect("/login/")

@app.route("/login/",methods=["POST","GET"])
def login():
    if request.method == "POST":
        _email = request.form["email"]
        _password = request.form["password"]
        _user = User.query.filter_by(email = _email).one()
        #print(_user.password)
        #_user = event_database.query(User).filter_by(email = _email).all()
        if _user.password == _password:
            session["email"] = _email
            #return redirect(url_for("login"))
            #return render_template("createevent.html")
            return redirect("/")
        else:
        #     have to define funtions to flash incorrect password message
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/Signup/", methods=["POST","GET"])
def create_account():
    if request.method == "POST":
        new_user = User(username = request.form["user_name"],email = request.form["email"],password = request.form["password"])
        if User.query.filter_by(email = request.form["email"]).first() != None:
            return redirect("/Signup/")
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    else:
        return render_template("signup.html")

@app.route("/Createevent/", methods =["POST","GET"])
def create_event():
    if request.method == "POST":
        eadmin = session["email"]
        icode = random.randint(100000,999999)
        new_event = Event(icode = icode,ename = request.form["event_name"],edesc = request.form["event_desc"],eadmin = eadmin)
        new_join = EventSec(icode = icode,ename = request.form["event_name"],member_email = eadmin)
        db.session.add(new_event)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("createevent.html")

@app.route("/Joinevent/", methods = ["POST","GET"])
def join_event():
    if request.method == "POST":
        _memail = session["email"]
        new_join = EventSec(icode = request.form["icode"],ename = request.form["ename"],member_email = _memail)
        db.session.add(new_join)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("joinevent.html")

if __name__ == "__main__":
    app.run(debug = True)

