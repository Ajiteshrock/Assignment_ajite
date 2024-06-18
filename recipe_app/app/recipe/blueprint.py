from flask import Blueprint
from app.recipe.routes import BaseRecipeView, CreateRecipeView, UpdateRecipeView, DeleteRecipeView

recipe_bp = Blueprint('recipes', __name__)
recipe_bp.add_url_rule('/recipes', view_func=BaseRecipeView.as_view('get_recipes'))
recipe_bp.add_url_rule('/recipes/<string:title>', view_func=BaseRecipeView.as_view('get_recipe_by_title'))
recipe_bp.add_url_rule('/recipes', view_func=CreateRecipeView.as_view('create_recipe'))
recipe_bp.add_url_rule('/recipes/<string:title>', view_func=UpdateRecipeView.as_view('update_recipe'))
recipe_bp.add_url_rule('/recipes/<string:title>', view_func=DeleteRecipeView.as_view('delete_recipe'))
