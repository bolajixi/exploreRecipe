import os
import openai


def generate_recipe(**kwargs):
    """
    Generate a recipe given a list of ingridents
    """
    openai.api_key = os.getenv(
        "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")

    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt="Write a recipe based on these ingredients and instructions:\n\nFrito Pie\n\nIngredients:\nFritos\nChili\nShredded cheddar cheese\nSweet white or red onions, diced small\nSour cream\n\nDirections:",
        temperature=0,
        max_tokens=120,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
