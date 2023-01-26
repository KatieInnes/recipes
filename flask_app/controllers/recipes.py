from flask import render_template, redirect, request, session 
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/recipes')
def recipes():
    if "id" not in session:
        return redirect('/logout')
    data = {
        "id": session["id"]
    }
    return render_template("recipes.html", user = User.search_by_id({"id": session["id"]}), recipes = Recipe.get_all())


@app.route('/recipes/new')
def create_recipe():
    if "id" not in session:
        return redirect('/logout')
    data = {
        "id": session["id"]
    }
    return render_template("create_recipe.html", user = User.search_by_id({"id": session["id"]}))


@app.route('/recipes/new', methods=["POST"])
def save_new_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    if "id" not in session:
        return redirect('/')

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30": int(request.form["under_30"]),
        "date_made": request.form["date_made"],
        "user_id": session["id"]
    }

    Recipe.save(data)
    return redirect('/recipes')


@app.route('/recipes/<int:id>')
def view_recipe(id):
    data = {
        "id": id
    }
    return render_template("view_recipe.html", recipe=Recipe.view_recipe(data), logged_in_user = User.search_by_id({"id": session["id"]}))

@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    
    if "id" not in session:
        return redirect('/logout')
    
    data = {
        "id": id
    }

    recipe = Recipe.view_recipe(data)

    if recipe and recipe.user == int(session["id"]):
        return render_template("edit_recipe.html", recipe=Recipe.view_recipe(data)) 

    return redirect("/recipes")

@app.route('/recipes/<int:id>/edit', methods=["POST"])
def update_recipe(id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/{id}/edit")

    data = {
        "id": request.form["id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30": int(request.form["under_30"]),
        "date_made": request.form["date_made"],
    }
    Recipe.edit_recipe(data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):

    if "id" not in session:
        return redirect('/logout')

    data = {
        "id": id
    }
    
    recipe = Recipe.view_recipe(data)

    if recipe and recipe.user == int(session["id"]):
        Recipe.delete_recipe(data)

    return redirect("/recipes")