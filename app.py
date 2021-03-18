from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pyusername = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)

db.create_all()

@app.route("/")
def dashboard():
    return redirect("/Signup")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.form == "POST":
        _email = request.form["email"]
        _password = request.form["password"]
        _user = User.query.filter_by(email = _email).one()
        if _user.password == _password:
            _name = _user.name
            return redirect("/")
        else:
            return redirect("/login")
    else:
        return redirect("/login")
    


@app.route("/Signup/", methods=["POST","GET"])
def create_account():
    if request.method == "GET":
        new_user = User(username = request.form("user_name"),email = request.form['email'],password = request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug = True)
