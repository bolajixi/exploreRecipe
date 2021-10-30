from django.conf import settings
from typing import List, Dict
import requests
import json


def get_nutrition(ingredients: List[str]) -> Dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "title": "not important",
        "ingr": ingredients
    }
    params = {
        "app_id": "18050ea7",
        "app_key": settings.EDAMAM_SECRET_KEY

    }
    url = "https://api.edamam.com/api/nutrition-details"
    response = requests.post(url, data=json.dumps(
        data), headers=headers, params=params)
    nut_res = response.json()
    nutrition = {}
    nutrition['calories'] = nut_res['calories']
    for _, nutrient in nut_res["totalNutrients"].items():
        nutrition[nutrient['label']] = str(
            round(nutrient['quantity'], ndigits=1)) + nutrient['unit']
    return nutrition
