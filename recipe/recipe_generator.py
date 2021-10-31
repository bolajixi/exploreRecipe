import os
import openai
import requests
from django.conf import settings
from typing import List, Dict


def generate_recipe(ingredients, recipe_name=None, **kwargs):
    """
    Generate a recipe given a list of ingredients

    """
    openai.api_key = settings.OPENAI_SECRET_KEY
    prompt_sentence = []

    if recipe_name:
        prompt = f"Write a recipe based on these ingredients and instructions:\n\n{recipe_name}\n\nIngredients:"
        prompt_sentence.append(prompt)
    else:
        prompt = "Write a recipe based on these ingredients and instructions:\n\nIngredients:"
        prompt_sentence.append(prompt)

    for ingredient in ingredients:
        prompt_sentence.append("\n" + ingredient)

    prompt_sentence.append("\nRecipe Name and Directions:")
    new_prompt = "".join(prompt_sentence)

    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        # prompt="Write a recipe based on these ingredients and instructions:\n\nFrito Pie\n\nIngredients:\nFritos\nChili\nShredded cheddar cheese\nSweet white or red onions, diced small\nSour cream\n\nDirections:",
        prompt=new_prompt,
        temperature=0,
        max_tokens=120,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    res = response.to_dict_recursive()
    recipe_str = res["choices"][0]["text"]
    return recipe_str.split("\n")


def get_ingredients(ingredient_dict_list, type="original"):
    ingredients = []
    for ingredient in ingredient_dict_list:
        ingredients.append(ingredient[type])
    return ingredients


def other_meal_ideas(ingredients: List[str]) -> List[Dict[str, str]]:
    params = {"apiKey": settings.SPOONACULAR_SECRET_KEY,
              #   "ingredients": "apples,+flour,+sugar",
              "ingredients": ",+".join(ingredients),
              #   uncommenting the below minimises missing ingredients rather than maximising used ones
              #   "ranking": "2",
              "number": "3",
              }
    response = requests.get(
        "https://api.spoonacular.com/recipes/findByIngredients", params=params)
    res = response.json()
    output = []
    for recipe in res:
        recipe_dict = {}
        full_ingredient = []

        recipe_dict['title'] = recipe['title']
        recipe_dict['image'] = recipe['image']

        recipe_dict['missedIngredients'] = get_ingredients(
            recipe['missedIngredients'])
        recipe_dict['usedIngredients'] = get_ingredients(
            recipe['usedIngredients'])

        for ingrident in get_ingredients(
                recipe['missedIngredients'], type='name'):
            full_ingredient.append(ingrident)

        for ingrident in get_ingredients(
                recipe['usedIngredients'], type='name'):
            full_ingredient.append(ingrident)

        recipe_dict['full_ingredient_list'] = ','.join(full_ingredient)
        output.append(recipe_dict)
    return output
