from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Post:
    DB = 'dojo_overflow'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    #Add post to database
    @classmethod
    def add_post_to_db(cls, data):
        query = """
        INSERT INTO posts 
        (title, content, users_id) 
        VALUES
        (%(title)s, %(content)s, %(user_id)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    #Get all posts from a single user
    @classmethod
    def get_posts_by_user_id(cls, data):
        query = """
        SELECT * FROM posts
        RIGHT JOIN users
        ON posts.users_id = users.id
        WHERE users.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        if len(results) == 0:
            return []
        else:
            all_posts_from_user_obj = []
            for post_dict in results:
                post_obj = Post(post_dict)
                user_dict = {
                    "id" : post_dict['users.id'],
                    "first_name" : post_dict['first_name'],
                    "last_name" : post_dict['last_name'],
                    "email" : post_dict['email'],
                    "password" : post_dict['password'],
                    "created_at" : post_dict['users.created_at'],
                    "updated_at" : post_dict['users.updated_at'],
                }
                user_obj = user.User(user_dict)
                post_obj.user = user_obj
                all_posts_from_user_obj.append(post_obj)
            return all_posts_from_user_obj
    
    #Get all posts
    @classmethod
    def get_all_posts(cls):
        query = """
        SELECT * FROM posts 
        JOIN users 
        ON posts.users_id = users.id;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        if len(results) == 0:
            return []
        else:
            all_posts_obj = []
            for post_dict in results:
                post_obj = Post(post_dict)
                user_dict = {
                    "id" : post_dict['users.id'],
                    "first_name" : post_dict['first_name'],
                    "last_name" : post_dict['last_name'],
                    "email" : post_dict['email'],
                    "password" : post_dict['password'],
                    "created_at" : post_dict['users.created_at'],
                    "updated_at" : post_dict['users.updated_at'],
                }
                user_obj = user.User(user_dict)
                post_obj.user = user_obj
                all_posts_obj.append(post_obj)
            return all_posts_obj
        
    #Get a single post
    @classmethod
    def get_post_by_id(cls, data):
        query = """
        SELECT * FROM posts 
        JOIN users 
        ON posts.users_id = users.id
        WHERE posts.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            post_dict = results[0]
            post_obj = Post(post_dict)
            user_dict = {
                "id" : post_dict['users.id'],
                "first_name" : post_dict['first_name'],
                "last_name" : post_dict['last_name'],
                "email" : post_dict['email'],
                "password" : post_dict['password'],
                "created_at" : post_dict['users.created_at'],
                "updated_at" : post_dict['users.updated_at'],
            }
            user_obj = user.User(user_dict)
            post_obj.user = user_obj
            return post_obj

    #Update a post on the database
    @classmethod
    def update_post_on_db(cls, data):
        query = """
        UPDATE posts 
        SET title = %(title)s, content = %(content)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    #Delete a post from the database
    @classmethod
    def delete_post_from_db(cls, data):
        query = """
        DELETE FROM posts 
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    #Like a post on the database
    @classmethod
    def like_post_on_db(cls, data):
        query = """
        INSERT INTO post_favorites (users_id, posts_id) 
        VALUES (%(user_id)s, %(post_id)s)
        ;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_liked_post_with_user(cls, data):
        # query = """
        # SELECT * FROM post_favorites 
        # LEFT JOIN posts 
        # ON post_favorites.posts_id = posts.id 
        # WHERE post_favorites.users_id = %(id)s
        # ;"""
        query = """
        SELECT * FROM post_favorites 
        LEFT JOIN posts 
        ON post_favorites.posts_id = posts.id 
        LEFT JOIN users ON posts.users_id = users.id
        WHERE post_favorites.users_id = %(id)s ;
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        return results


    #Validations
    @staticmethod
    def validate_post(form_data):
        is_valid = True
        if len(form_data['title']) < 3:
            flash('Title must be at least 3 characters long')
            is_valid = False
        if len(form_data['content']) < 10:
            flash('Content must be at least 10 characters long')
            is_valid = False
        return is_valid