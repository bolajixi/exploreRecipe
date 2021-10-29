from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('explore/', views.explore_recipe, name='recipe'),
]
