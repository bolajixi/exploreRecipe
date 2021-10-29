import os
import openai
from django.conf import settings


def generate_recipe(ingridents, **kwargs):
    """
    Generate a recipe given a list of ingridents
    """
    openai.api_key = os.getenv(
        settings.OPENAI_SECRET_KEY)

    prompt_list = [
        "Write a recipe based on these ingredients and instructions:"]

    for ingrident in ingridents:
        prompt_list.append("\n"+ingrident)

    prompt = "".join(prompt_list)

    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        # prompt="Write a recipe based on these ingredients and instructions:\n\nFrito Pie\n\nIngredients:\nFritos\nChili\nShredded cheddar cheese\nSweet white or red onions, diced small\nSour cream\n\nDirections:",
        prompt=prompt_list,
        temperature=0,
        max_tokens=120,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
