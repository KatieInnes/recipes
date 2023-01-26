from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.recipe_name = data['name']
        self.recipe_description = data['description']
        self.recipe_instructions = data['instructions']
        self.under_30_minutes = data['under_30']
        self.date_recipe_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data['user_id']

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True

        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False

        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False

        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False

        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes"
        results = connectToMySQL("recipes").query_db(query)

        recipes = []
        for item in results:
            recipes.append(cls(item))
        return recipes

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO 
            recipes 
            (name, description, instructions, under_30, date_made, user_id) 
        VALUES
            (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s, %(user_id)s)
        """
        return connectToMySQL("recipes").query_db(query, data) 

    @classmethod
    def get_user_with_recipes (cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL("recipes").query_db(query, data)
        return results

    @classmethod
    def view_recipe(cls, data):
        query = """
            SELECT * FROM 
                recipes 
            LEFT JOIN users on recipes.user_id = users.id
            WHERE recipes.id = %(id)s
        """
        result = connectToMySQL("recipes").query_db(query, data)
        return cls(result[0])

    @classmethod
    def edit_recipe(cls, data):
        query = """
        UPDATE 
            recipes SET 
            name=%(name)s, description=%(description)s, instructions=%(instructions)s,under_30=%(under_30)s, date_made=%(date_made)s
        WHERE id = %(id)s
        """
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = """
        DELETE FROM 
            recipes 
            WHERE id = %(id)s
        """
        return connectToMySQL("recipes").query_db(query, data)