from flask_app import app
from flask import Flask, render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.post import Post

from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/new-user', methods=["POST"])
def create_user():
    print("create_user -->", request.form)
    if not User.validate_create(request.form):
        return redirect('/')
    user_id = User.create(request.form)
    session['user_id'] = user_id
    return redirect ('/dashboard')


@app.route('/dashboard')
def user_page():
    if "user_id" not in session:
        return ('/')
    data = {
        "id": session['user_id']
    }
    return render_template("user-dashboard.html", logged_in_user = User.get_user_id(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
