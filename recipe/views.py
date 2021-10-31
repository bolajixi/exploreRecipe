from django.core.exceptions import NON_FIELD_ERRORS
from django.shortcuts import render
from .recipe_generator import generate_recipe
from .forms import IngredientForm
from .models import Ingredient
from django.forms import modelformset_factory
from .recipe_generator import generate_recipe, other_meal_ideas

import ast

# Create your views here.


def explore_recipe(request):

    recipe_name, directions, other_ideas = None, None, None

    ingredients = list()
    IngredientFormset = modelformset_factory(
        Ingredient, IngredientForm, extra=3)

    if request.method == "GET":
        formset = IngredientFormset(request.GET or None)
        return render(request, 'recipe/index.html', {'formset': formset, })

    elif request.method == "POST":
        formset = IngredientFormset(request.POST)

        if formset.is_valid():
            for form in formset.cleaned_data:
                if form:
                    ingredients.append(form['name'])

            recipe = generate_recipe(ingredients=ingredients)
            recipe_name = recipe[2] if recipe and not recipe[0].isnumeric(
            ) else None
            directions = recipe[3:] if recipe else None
            other_ideas = other_meal_ideas(ingredients)

            context_data = {'recipe_name': recipe_name,
                            'recipe': directions,
                            'other_ideas': other_ideas,
                            'ingredients': ingredients,
                            }
            return render(request, 'recipe/generated_recipe.html', context=context_data)

        else:
            print(formset.errors)


def explore_other_recipe(request):

    if request.method == 'POST':
        print('hello')

        ingredients_data = request.POST['full_ingredient_list']
        ingredients_data = ingredients_data.strip().split(',')

        recipe = generate_recipe(ingredients=ingredients_data)
        recipe_name = recipe[2] if recipe and not recipe[0].isnumeric(
        ) else None
        directions = recipe[3:] if recipe else None
        other_ideas = other_meal_ideas(ingredients_data)

        context_data = {'recipe_name': recipe_name,
                        'recipe': directions,
                        'other_ideas': other_ideas,
                        'ingredients': ingredients_data,
                        }
        return render(request, 'recipe/generated_recipe.html', context=context_data)

    # return HttpResponse('/')
