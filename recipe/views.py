from django.shortcuts import render
from .recipe_generator import generate_recipe
from .forms import IngredientForm
from .models import Ingredient
from django.forms import modelformset_factory

# Create your views here.


def explore_recipe(request):

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

            print(ingredients)
            recipe = generate_recipe(ingredients=ingredients)
            return render(request, 'recipe/result.html', {'recipe': recipe, })
        else:
            print(formset.errors)
