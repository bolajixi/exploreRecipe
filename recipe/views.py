from django.shortcuts import render
from .recipe_generator import generate_recipe, other_meal_ideas

# Create your views here.


def explore_recipe(request):
    ingredients1 = ["Ball pepper", "Tomatoes", "Spinach"]
    ingredients = ["new potatoes", "oil",
                   "leeks", "eggs", "pepper smoked mackerel", "creamed horseradish"]
    recipe = generate_recipe(ingredients=ingredients)
    recipe_name = recipe[2] if recipe and not recipe[0].isnumeric() else None
    directions = recipe[3:] if recipe else None
    other_ideas = other_meal_ideas(ingredients)

    context_data = {'recipe_name': recipe_name,
                    'recipe': directions,
                    'other_ideas': other_ideas,
                    'ingredients': ingredients,
                    }
    return render(request, 'recipe/generated_recipe.html', context=context_data)
