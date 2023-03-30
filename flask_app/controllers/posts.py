from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, post

#Visible routes

#Route that shows create post form and all posts created by logged in user.
@app.route('/posts/my_posts')
def user_posts_and_create_page():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id'],
    }
    return render_template('my_posts.html', logged_in_user = user.User.get_user_id(data), 
                           posts_by_user = post.Post.get_posts_by_user_id(data), 
                           liked_posts = post.Post.get_liked_post_with_user(data), 
                           all_posts=post.Post.get_all_posts())


#Route that shows edit post page
@app.route('/posts/edit/<int:id>')
def edit_post_page(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': id,
    }
    return render_template('editpost.html', this_post = post.Post.get_post_by_id(data))


#Invisible routes

#Route to create a post
@app.route('/posts/create', methods = ['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/')
    if not post.Post.validate_post(request.form):
        return redirect('/posts/my_posts')
    data = {
        'title': request.form['title'],
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    post.Post.add_post_to_db(data)
    print("CREATE POST -->",data)
    return redirect('/posts/my_posts')


#Route to update a post
@app.route('/update/post/<int:id>', methods = ['POST'])
def update_post(id):
    if 'user_id' not in session:
        return redirect('/')
    if not post.Post.validate_post(request.form):
        return redirect(f'/posts/edit/{id}')
    data = {
        'title': request.form['title'],
        'content': request.form['content'],
        'id': id
    }
    post.Post.update_post_on_db(data)
    return redirect('/posts/my_posts')


#Route to link a post to a user when they click the like button.
@app.route('/posts/like/<int:id>', methods = ['POST'])
def like_post(id):
    if 'user_id' not in session:
        return redirect('/')
    user_post_ids = {
        'post_id': id,
        'user_id': session['user_id']
    }
    if not post.Post.validate_like(user_post_ids):
        return redirect('/dashboard')
    post.Post.get_like_by_user_post_id(user_post_ids)
    data ={
        'post_id': id,
        'user_id': session['user_id']
    }
    post.Post.like_post_on_db(data)
    return redirect('/dashboard')


#Route to delete a post
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': id,
    }
    post.Post.delete_post_from_db(data)
    return redirect('/posts/my_posts')