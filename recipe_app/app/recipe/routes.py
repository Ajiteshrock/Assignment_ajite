from flask import request, jsonify, current_app as app
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth.models import User
from app.recipe.model_repos.recipe_repo import RecipeRepository
from sqlalchemy.exc import SQLAlchemyError

class BaseRecipeView(MethodView):
    def get(self, title=None):
        if title:
            return self.get_recipe_by_title(title)
        else:
            return self.get_all_recipes()

    def get_all_recipes(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search_query = request.args.get('search', '', type=str)

        try:
            paginated_recipes = RecipeRepository.get_recipes(page, per_page, search_query)
            recipes = paginated_recipes.items
            output = [
                {
                    'id': recipe.id,
                    'title': recipe.title,
                    'description': recipe.description,
                    'ingredients': [{'name': ing.name, 'quantity': ing.quantity} for ing in recipe.ingredients],
                    'instructions': recipe.instructions
                }
                for recipe in recipes
            ]
            meta = {
                'page': paginated_recipes.page,
                'pages': paginated_recipes.pages,
                'per_page': paginated_recipes.per_page,
                'total': paginated_recipes.total
            }
            return jsonify({
                'meta': meta,
                'recipes': output
            }), 200
        except SQLAlchemyError as e:
            app.logger.error(f"Error fetching recipes: {str(e)}")
            return jsonify({'message': 'An error occurred while fetching the recipes'}), 500
        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            return jsonify({'message': str(e)}), 500

    def get_recipe_by_title(self, title):
        try:
            recipe = RecipeRepository.get_recipe_by_title(title)
            return jsonify({
                'id': recipe.id,
                'title': recipe.title,
                'description': recipe.description,
                'ingredients': [{'name': ing.name, 'quantity': ing.quantity} for ing in recipe.ingredients],
                'instructions': recipe.instructions
            }), 200
        except SQLAlchemyError as e:
            app.logger.error(f"Error fetching recipe: {str(e)}")
            return jsonify({'message': 'An error occurred while fetching the recipe'}), 500
        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            return jsonify({'message': str(e)}), 500

class CreateRecipeView(MethodView):

    @jwt_required()
    def post(self):
        data = request.get_json()
        required_fields = ['title', 'ingredients', 'instructions']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400

        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user['username']).first()

        try:
            new_recipe = RecipeRepository.create_recipe(data, user)
            return jsonify({
                'message': 'Recipe created successfully',
                'recipe': {
                    'id': new_recipe.id,
                    'title': new_recipe.title,
                    'description': new_recipe.description,
                    'ingredients': [{'name': ing.name, 'quantity': ing.quantity} for ing in new_recipe.ingredients],
                    'instructions': new_recipe.instructions,
                    'created_by': new_recipe.author.username
                }
            }), 201
        except SQLAlchemyError as e:
            app.logger.error(f"Error creating recipe: {str(e)}")
            return jsonify({'message': 'An error occurred while creating the recipe'}), 500
        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            return jsonify({'message': str(e)}), 500

class UpdateRecipeView(MethodView):

    @jwt_required()
    def put(self, title):
        data = request.get_json()
        required_fields = ['title', 'ingredients', 'instructions']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400

        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user['username']).first()

        try:
            recipe, status_code = RecipeRepository.update_recipe(title, data, user)
            if status_code == 403:
                return jsonify({'message': 'You can only edit your own recipes'}), 403
            return jsonify({'message': 'Recipe updated successfully'}), 200
        except SQLAlchemyError as e:
            app.logger.error(f"Error updating recipe: {str(e)}")
            return jsonify({'message': 'An error occurred while updating the recipe'}), 500
        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            return jsonify({'message': str(e)}), 500

class DeleteRecipeView(MethodView):

    @jwt_required()
    def delete(self, title):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user['username']).first()

        try:
            recipe, status_code = RecipeRepository.delete_recipe(title, user)
            if status_code == 403:
                return jsonify({'message': 'You can only delete your own recipes'}), 403
            return jsonify({'message': 'Recipe deleted successfully'}), 200
        except SQLAlchemyError as e:
            app.logger.error(f"Error deleting recipe: {str(e)}")
            return jsonify({'message': 'An error occurred while deleting the recipe'}), 500
        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            return jsonify({'message': str(e)}), 500