from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, post

#Visible routes

#Route that shows create post form and all posts created by logged in user.
@app.route('/posts/my_posts')
def user_posts_and_create_page():
    if 'user_id' not in session:
        redirect('/')
    data ={
        'id': session['user_id'],
    }
    return render_template('my_posts.html', logged_in_user = user.User.get_user_id(data), posts_by_user = post.Post.get_posts_by_user_id(data))


#Route that shows edit post page
@app.route('/posts/edit/<int:id>')
def edit_post_page(id):
    if 'user_id' not in session:
        redirect('/')
    data ={
        'id': id,
    }
    return render_template('editpost.html', this_post = post.Post.get_post_by_id(data))


#Invisible routes

#Route to create a post
@app.route('/posts/create', methods = ['POST'])
def create_post():
    if 'user_id' not in session:
        redirect('/')
    if not post.Post.validate_post(request.form):
        return redirect('/posts/my_posts')
    data = {
        'title': request.form['title'],
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    post.Post.add_post_to_db(data)
    return redirect('/posts/my_posts')


#Route to update a post
@app.route('/update/post/<int:id>', methods = ['POST'])
def update_post(id):
    if 'user_id' not in session:
        redirect('/')
    if not post.Post.validate_post(request.form):
        return redirect(f'/posts/edit/{id}')
    data = {
        'title': request.form['title'],
        'content': request.form['content'],
        'id': id
    }
    post.Post.update_post_on_db(data)
    return redirect('/posts/my_posts')


#Route to delete a post
@app.route('/posts/delete/<int:id>', methods = ['POST'])
def delete_post(id):
    if 'user_id' not in session:
        redirect('/')
    data ={
        'id': id,
    }
    post.Post.delete_post_from_db(data)
    return redirect('/posts/my_posts')