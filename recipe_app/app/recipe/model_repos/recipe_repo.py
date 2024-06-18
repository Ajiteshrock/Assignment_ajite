from app import db
from app.recipe.models import Recipe, Ingredient

class RecipeRepository:

    @staticmethod
    def create_recipe(data, user):
        new_recipe = Recipe(
            title=data['title'], 
            description=data.get('description'), 
            instructions=data.get('instructions'), 
            author=user
        )
        db.session.add(new_recipe)
        db.session.flush()  # Get the ID of the new recipe before committing

        ingredients = data.get('ingredients', [])
        for ing in ingredients:
            ingredient = Ingredient(name=ing['name'], quantity=ing.get('quantity'), recipe_id=new_recipe.id)
            db.session.add(ingredient)

        db.session.commit()
        return new_recipe

    @staticmethod
    def get_recipes(page, per_page, search_query):
        query = Recipe.query.options(db.joinedload(Recipe.ingredients))
        
        if search_query:
            query = query.filter((Recipe.title.ilike(f'%{search_query}%')) | (Recipe.ingredients.any(Ingredient.name.ilike(f'%{search_query}%'))))

        paginated_recipes = query.paginate(page=page, per_page=per_page, error_out=False)
        return paginated_recipes

    @staticmethod
    def get_recipe_by_title(title):
        return Recipe.query.options(db.joinedload(Recipe.ingredients)).filter_by(title=title).first_or_404()

    @staticmethod
    def update_recipe(title, data, user):
        recipe = Recipe.query.filter_by(title=title).first_or_404()

        if recipe.author != user:
            return None, 403

        recipe.title = data['title']
        recipe.description = data.get('description')
        recipe.instructions = data.get('instructions')

        Ingredient.query.filter_by(recipe_id=recipe.id).delete()
        ingredients = data.get('ingredients', [])
        for ing in ingredients:
            ingredient = Ingredient(name=ing['name'], quantity=ing.get('quantity'), recipe_id=recipe.id)
            db.session.add(ingredient)

        db.session.commit()
        return recipe, 200

    @staticmethod
    def delete_recipe(title, user):
        recipe = Recipe.query.filter_by(title=title).first_or_404()

        if recipe.author != user:
            return None, 403

        Ingredient.query.filter_by(recipe_id=recipe.id).delete()
        db.session.delete(recipe)
        db.session.commit()
        return recipe, 200
