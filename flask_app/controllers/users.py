from flask import render_template, flash, redirect, request, session 
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registration', methods=["POST"])
def register_new_user():
    if not User.validate_user_registration(request.form):
        return redirect('/')

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }

    id = User.save(data)
    session["id"] = id
    return redirect('/recipes')

@app.route('/login', methods=["POST"])
def login():
    user_in_database = User.search_by_email(request.form)
    if not user_in_database: 
        flash("Invalid email/password")
        return redirect ('/')
        
    if not bcrypt.check_password_hash(user_in_database.password, request.form['password']):
        flash("Invalid email/password")
        return redirect ('/')
    session["id"] = user_in_database.id
    return redirect('/recipes')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')