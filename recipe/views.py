from django.shortcuts import render
from .recipe_generator import generate_recipe, other_meal_ideas

# Create your views here.


def explore_recipe(request):
    ingredients1 = ["Ball pepper", "Tomatoes", "Spinach"]
    ingredients = ["new potatoes", "oil",
                   "leeks", "eggs", "pepper smoked mackerel", "creamed horseradish"]
    recipe = generate_recipe(ingredients=ingredients)
    other_ideas = other_meal_ideas(ingredients)

    context_data = {'recipe': recipe,
                    'other_ideas': other_ideas,
                    'ingredients': ingredients,
                    }
    return render(request, 'recipe/generated_recipe.html', context=context_data)
