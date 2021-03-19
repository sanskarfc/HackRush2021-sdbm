from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///event_database.db"
db = SQLAlchemy(app)

class User(db.Model):
    #id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, primary_key = True)
    password = db.Column(db.String(100), nullable = False)

db.create_all()

@app.route("/")
def dashboard():
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
            #session["email"] = _email
            #return redirect(url_for("login"))
            return render_template("createevent.html")
        else:
        #     have to define funtions to flash incorrect password message
            return render_template("login.html")
    else:
        return render_template("login.html")
    


@app.route("/Signup/", methods=["POST","GET"])
def create_account():
    if request.method == "POST":
        new_user = User(username = request.form["user_name"],email = request.form['email'],password = request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    else:
        return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug = True)

