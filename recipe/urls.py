from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.explore_recipe, name='recipe'),
    path('nutrition', views.explore_nutrition, name='recipe'),

]
