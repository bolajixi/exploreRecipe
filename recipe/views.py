from django.shortcuts import render
from .recipe_generator import generate_recipe

# Create your views here.


def explore_recipe(request):
    ingredients = ["Ball pepper", "Tomatoes", "Spinach"]
    recipe = generate_recipe(ingredients=ingredients)

    context_data = recipe
    return render(request, 'recipe/index.html', context=context_data)
