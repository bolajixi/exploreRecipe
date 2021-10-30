from django.core.exceptions import NON_FIELD_ERRORS
from django.shortcuts import render
from .recipe_generator import generate_recipe
from .forms import IngredientForm
from .models import Ingredient
from django.forms import modelformset_factory
from .recipe_generator import generate_recipe, other_meal_ideas
from .nutrition import get_nutrition
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


def explore_nutrition(request):
    # todo: create/reuse some form to take ingredients
    ingredients = ["2 small green peppers, coarsely chopped",
                   "2 C long grain brown rice, cooked",
                   "1 lb pound extra - lean ground beef",
                   "1 tsp onion powder",
                   "3 garlic cloves, minced",
                   "1 24oz jar of low - sodium spaghetti sauce(If you are using a plain spaghetti sauce, you will want to add in 1 / 4 tsp Italian seasoning, 2 tsp season salt, 2 tsp onion powder, and 1 1 / 2 tsp garlic powder to give more flavor.)",
                   "1 1 / 2 C reduced - fat mozzarella cheese blend, divided"]
    # print(get_nutrition(ingredients))
    context_data = {
        "nutrition": get_nutrition(ingredients),
        "ingredients": ingredients
    }
    return render(request, 'recipe/nutrition.html', context=context_data)
