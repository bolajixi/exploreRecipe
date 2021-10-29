import os
import openai
from django.conf import settings


def generate_recipe(ingredients, **kwargs):
    """
    Generate a recipe given a list of ingridents

    """
    openai.api_key = os.getenv(
        settings.OPENAI_SECRET_KEY)

    prompt_sentence = [
        "Write a recipe based on these ingredients and instructions:\n\nIngredients:"]

    for ingredient in ingredients:
        prompt_sentence.append("\n"+ingredient)

    prompt_sentence.append("\n\nDirections:")
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
    return res["choices"][0]["text"]
