from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Post:
    DB = 'dojo_overflow'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        #Validations
        @staticmethod
        def validate_post(form_data):
            is_valid = True
            if len(form_data['title']) < 3:
                flash('Title must be at least 3 characters long')
                is_valid = False
            elif len(form_data['content']) < 10:
                flash('Content must be at least 10 characters long')
                is_valid = False
            return is_valid