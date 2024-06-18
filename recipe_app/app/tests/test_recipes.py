import pytest
from flask_jwt_extended import create_access_token, JWTManager
from app import create_app, db
from app.auth.models import User

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/recipes_db'
    flask_app.config['JWT_SECRET_KEY'] = 'test_jwt_secret_key'

    testing_client = flask_app.test_client()

    with flask_app.app_context():
        db.create_all()
        jwt_manager = JWTManager(flask_app)
        create_test_user(flask_app)
        token = get_auth_token(flask_app)

        yield testing_client, token

        db.session.remove()
        db.drop_all()

def create_test_user(flask_app):
    username = 'testuser'
    password = 'testpassword'
    user = User(username=username)
    user.password = password
    db.session.add(user)
    db.session.commit()

def get_auth_token(flask_app):
    with flask_app.app_context():
        return create_access_token(identity={'username': 'testuser'})

def test_create_recipe(test_client):
    client, token = test_client
    recipe_payload = {
        "title": "Vegetable Stir Fry",
        "description": "A healthy and colorful vegetable stir fry with a savory sauce.",
        "ingredients": [
            {"name": "broccoli", "quantity": "1 cup"},
            {"name": "carrot", "quantity": "1 large, sliced"},
            {"name": "red bell pepper", "quantity": "1, sliced"},
            {"name": "snow peas", "quantity": "1 cup"},
            {"name": "mushrooms", "quantity": "1 cup, sliced"},
            {"name": "garlic", "quantity": "2 cloves, minced"},
            {"name": "ginger", "quantity": "1 tbsp, minced"},
            {"name": "soy sauce", "quantity": "3 tbsp"},
            {"name": "sesame oil", "quantity": "1 tbsp"},
            {"name": "olive oil", "quantity": "2 tbsp"},
            {"name": "cornstarch", "quantity": "1 tsp"},
            {"name": "water", "quantity": "1/4 cup"},
            {"name": "green onions", "quantity": "2, chopped"},
            {"name": "sesame seeds", "quantity": "1 tsp, for garnish"}
        ],
        "instructions": "1. Heat olive oil in a large skillet or wok over medium-high heat. 2. Add minced garlic and ginger, and cook for 1 minute until fragrant. 3. Add broccoli, carrot, and red bell pepper, and stir fry for 3-4 minutes. 4. Add snow peas and mushrooms, and continue to stir fry for another 2-3 minutes until vegetables are tender-crisp. 5. In a small bowl, mix soy sauce, sesame oil, cornstarch, and water until smooth. 6. Pour the sauce over the vegetables and stir well to coat evenly. 7. Cook for another 1-2 minutes until the sauce thickens. 8. Remove from heat and sprinkle with chopped green onions and sesame seeds. Serve hot."
    }
    response = client.post('/recipes', 
                           headers={'Authorization': f'Bearer {token}'},
                           json=recipe_payload)
    assert response.status_code == 201
    assert 'Recipe created successfully' in response.get_json()['message']

def test_get_recipes(test_client):
    client, token = test_client
    recipe_payload = {
        "title": "Vegetable Stir Fry",
        "description": "A healthy and colorful vegetable stir fry with a savory sauce.",
        "ingredients": [
            {"name": "broccoli", "quantity": "1 cup"},
            {"name": "carrot", "quantity": "1 large, sliced"},
            {"name": "red bell pepper", "quantity": "1, sliced"},
            {"name": "snow peas", "quantity": "1 cup"},
            {"name": "mushrooms", "quantity": "1 cup, sliced"},
            {"name": "garlic", "quantity": "2 cloves, minced"},
            {"name": "ginger", "quantity": "1 tbsp, minced"},
            {"name": "soy sauce", "quantity": "3 tbsp"},
            {"name": "sesame oil", "quantity": "1 tbsp"},
            {"name": "olive oil", "quantity": "2 tbsp"},
            {"name": "cornstarch", "quantity": "1 tsp"},
            {"name": "water", "quantity": "1/4 cup"},
            {"name": "green onions", "quantity": "2, chopped"},
            {"name": "sesame seeds", "quantity": "1 tsp, for garnish"}
        ],
        "instructions": "1. Heat olive oil in a large skillet or wok over medium-high heat. 2. Add minced garlic and ginger, and cook for 1 minute until fragrant. 3. Add broccoli, carrot, and red bell pepper, and stir fry for 3-4 minutes. 4. Add snow peas and mushrooms, and continue to stir fry for another 2-3 minutes until vegetables are tender-crisp. 5. In a small bowl, mix soy sauce, sesame oil, cornstarch, and water until smooth. 6. Pour the sauce over the vegetables and stir well to coat evenly. 7. Cook for another 1-2 minutes until the sauce thickens. 8. Remove from heat and sprinkle with chopped green onions and sesame seeds. Serve hot."
    }
    client.post('/recipes', 
                headers={'Authorization': f'Bearer {token}'},
                json=recipe_payload)

    response = client.get('/recipes',
                          headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'meta' in response.get_json()
    assert 'recipes' in response.get_json()

def test_get_recipe_by_title(test_client):
    client, token = test_client
    recipe_payload = {
        "title": "Vegetable Stir Fry",
        "description": "A healthy and colorful vegetable stir fry with a savory sauce.",
        "ingredients": [
            {"name": "broccoli", "quantity": "1 cup"},
            {"name": "carrot", "quantity": "1 large, sliced"},
            {"name": "red bell pepper", "quantity": "1, sliced"},
            {"name": "snow peas", "quantity": "1 cup"},
            {"name": "mushrooms", "quantity": "1 cup, sliced"},
            {"name": "garlic", "quantity": "2 cloves, minced"},
            {"name": "ginger", "quantity": "1 tbsp, minced"},
            {"name": "soy sauce", "quantity": "3 tbsp"},
            {"name": "sesame oil", "quantity": "1 tbsp"},
            {"name": "olive oil", "quantity": "2 tbsp"},
            {"name": "cornstarch", "quantity": "1 tsp"},
            {"name": "water", "quantity": "1/4 cup"},
            {"name": "green onions", "quantity": "2, chopped"},
            {"name": "sesame seeds", "quantity": "1 tsp, for garnish"}
        ],
        "instructions": "1. Heat olive oil in a large skillet or wok over medium-high heat. 2. Add minced garlic and ginger, and cook for 1 minute until fragrant. 3. Add broccoli, carrot, and red bell pepper, and stir fry for 3-4 minutes. 4. Add snow peas and mushrooms, and continue to stir fry for another 2-3 minutes until vegetables are tender-crisp. 5. In a small bowl, mix soy sauce, sesame oil, cornstarch, and water until smooth. 6. Pour the sauce over the vegetables and stir well to coat evenly. 7. Cook for another 1-2 minutes until the sauce thickens. 8. Remove from heat and sprinkle with chopped green onions and sesame seeds. Serve hot."
    }
    client.post('/recipes', 
                headers={'Authorization': f'Bearer {token}'},
                json=recipe_payload)

    response = client.get('/recipes/Vegetable%20Stir%20Fry',
                          headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'title' in response.get_json()
    assert response.get_json()['title'] == 'Vegetable Stir Fry'

def test_update_recipe(test_client):
    client, token = test_client
    recipe_payload = {
        "title": "Vegetable Stir Fry",
        "description": "A healthy and colorful vegetable stir fry with a savory sauce.",
        "ingredients": [
            {"name": "broccoli", "quantity": "1 cup"},
            {"name": "carrot", "quantity": "1 large, sliced"},
            {"name": "red bell pepper", "quantity": "1, sliced"},
            {"name": "snow peas", "quantity": "1 cup"},
            {"name": "mushrooms", "quantity": "1 cup, sliced"},
            {"name": "garlic", "quantity": "2 cloves, minced"},
            {"name": "ginger", "quantity": "1 tbsp, minced"},
            {"name": "soy sauce", "quantity": "3 tbsp"},
            {"name": "sesame oil", "quantity": "1 tbsp"},
            {"name": "olive oil", "quantity": "2 tbsp"},
            {"name": "cornstarch", "quantity": "1 tsp"},
            {"name": "water", "quantity": "1/4 cup"},
            {"name": "green onions", "quantity": "2, chopped"},
            {"name": "sesame seeds", "quantity": "1 tsp, for garnish"}
        ],
        "instructions": "1. Heat olive oil in a large skillet or wok over medium-high heat. 2. Add minced garlic and ginger, and cook for 1 minute until fragrant. 3. Add broccoli, carrot, and red bell pepper, and stir fry for 3-4 minutes. 4. Add snow peas and mushrooms, and continue to stir fry for another 2-3 minutes until vegetables are tender-crisp. 5. In a small bowl, mix soy sauce, sesame oil, cornstarch, and water until smooth. 6. Pour the sauce over the vegetables and stir well to coat evenly. 7. Cook for another 1-2 minutes until the sauce thickens. 8. Remove from heat and sprinkle with chopped green onions and sesame seeds. Serve hot."
    }
    client.post('/recipes', 
                headers={'Authorization': f'Bearer {token}'},
                json=recipe_payload)

    updated_recipe_payload = {
        "title": "Updated Vegetable Stir Fry",
        "description": "An updated version of a healthy and colorful vegetable stir fry with a savory sauce.",
        "ingredients": [
            {"name": "broccoli", "quantity": "1 cup"},
            {"name": "carrot", "quantity": "1 large, sliced"},
            {"name": "red bell pepper", "quantity": "1, sliced"},
            {"name": "snow peas", "quantity": "1 cup"},
            {"name": "mushrooms", "quantity": "1 cup, sliced"},
            {"name": "garlic", "quantity": "2 cloves, minced"},
            {"name": "ginger", "quantity": "1 tbsp, minced"},
            {"name": "soy sauce", "quantity": "3 tbsp"},
            {"name": "sesame oil", "quantity": "1 tbsp"},
            {"name": "olive oil", "quantity": "2 tbsp"},
            {"name": "cornstarch", "quantity": "1 tsp"},
            {"name": "water", "quantity": "1/4 cup"},
            {"name": "green onions", "quantity": "2, chopped"},
            {"name": "sesame seeds", "quantity": "1 tsp, for garnish"}
        ],
        "instructions": "1. Heat olive oil in a large skillet or wok over medium-high heat. 2. Add minced garlic and ginger, and cook for 1 minute until fragrant. 3. Add broccoli, carrot, and red bell pepper, and stir fry for 3-4 minutes. 4. Add snow peas and mushrooms, and continue to stir fry for another 2-3 minutes until vegetables are tender-crisp. 5. In a small bowl, mix soy sauce, sesame oil, cornstarch, and water until smooth. 6. Pour the sauce over the vegetables and stir well to coat evenly. 7. Cook for another 1-2 minutes until the sauce thickens. 8. Remove from heat and sprinkle with chopped green onions and sesame seeds. Serve hot."
    }

    response = client.put('/recipes/Vegetable%20Stir%20Fry', 
                          headers={'Authorization': f'Bearer {token}'},
                          json=updated_recipe_payload)
    assert response.status_code == 200
    assert 'Recipe updated successfully' in response.get_json()['message']

def test_delete_recipe(test_client):
    client, token = test_client
    recipe_payload = {
        "title": "Vegetable Stir Fry",
        "description": "A healthy and colorful vegetable stir fry with a savory sauce.",
        "ingredients": [
            {"name": "broccoli", "quantity": "1 cup"},
            {"name": "carrot", "quantity": "1 large, sliced"},
            {"name": "red bell pepper", "quantity": "1, sliced"},
            {"name": "snow peas", "quantity": "1 cup"},
            {"name": "mushrooms", "quantity": "1 cup, sliced"},
            {"name": "garlic", "quantity": "2 cloves, minced"},
            {"name": "ginger", "quantity": "1 tbsp, minced"},
            {"name": "soy sauce", "quantity": "3 tbsp"},
            {"name": "sesame oil", "quantity": "1 tbsp"},
            {"name": "olive oil", "quantity": "2 tbsp"},
            {"name": "cornstarch", "quantity": "1 tsp"},
            {"name": "water", "quantity": "1/4 cup"},
            {"name": "green onions", "quantity": "2, chopped"},
            {"name": "sesame seeds", "quantity": "1 tsp, for garnish"}
        ],
        "instructions": "1. Heat olive oil in a large skillet or wok over medium-high heat. 2. Add minced garlic and ginger, and cook for 1 minute until fragrant. 3. Add broccoli, carrot, and red bell pepper, and stir fry for 3-4 minutes. 4. Add snow peas and mushrooms, and continue to stir fry for another 2-3 minutes until vegetables are tender-crisp. 5. In a small bowl, mix soy sauce, sesame oil, cornstarch, and water until smooth. 6. Pour the sauce over the vegetables and stir well to coat evenly. 7. Cook for another 1-2 minutes until the sauce thickens. 8. Remove from heat and sprinkle with chopped green onions and sesame seeds. Serve hot."
    }
    client.post('/recipes', 
                headers={'Authorization': f'Bearer {token}'},
                json=recipe_payload)

    response = client.delete('/recipes/Vegetable%20Stir%20Fry', 
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'Recipe deleted successfully' in response.get_json()['message']