from django.shortcuts import render
from .recipe_generator import generate_recipe

# Create your views here.


def explore_recipe(request):
    ingredients = ["Ball pepper", "Tomatoes", "Spinach"]
    recipe = generate_recipe(ingredients=ingredients)

    print(recipe)
    # return render(request, 'shop/product/list.html', context_data)
