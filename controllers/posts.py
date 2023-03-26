from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, post

#Visible routes
#Route that shows create post form and all posts created by logged in user.
@app.route('/posts/my_posts')
def all_and_create_posts():
    if 'user_id' not in session:
        redirect('/')
    
    data ={
        'id': session['user_id'],
    }
    return render_template('my_posts.html', logged_in_user = user.User.get_user_id(data))

#Route that shows edit post page
@app.route('/posts/edit/<int:id>', methods = ['POST'])
def edit_post(id):
    if 'user_id' not in session:
        redirect('/')
    
    data ={
        'id': session['user_id'],
    }
    return render_template('editpost.html')

#Invisible routes
#Route to delete a post
@app.route('/posts/delete/<int:id>', methods = ['POST'])
def delete_post(id):
    if 'user_id' not in session:
        redirect('/')
    
    data ={
        'id': session['user_id'],
    }
    return redirect('/posts/my_posts')

#Route to create a post
@app.route('/posts/create', methods = ['POST'])
def create_post():
    if 'user_id' not in session:
        redirect('/')

    data = {
        'id': session['user_id'],
    }
    return redirect('/posts/my_posts')

#Route to update a post
@app.route('/posts/update/<int:id>', methods = ['POST'])
def update_post(id):
    if 'user_id' not in session:
        redirect('/')
    
    data = {
        'id': session['user_id'],
    }
    return redirect('/posts/my_posts')
