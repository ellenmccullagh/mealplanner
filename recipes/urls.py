from django.conf.urls import url
from . import views
from recipes.models import Recipe

urlpatterns = [
                url(r'^$', views.index, name='index'),
                url(r'^recipe/new/$', views.recipe_new, name='recipe_new'),
                url(r'^recipe/url/$', views.recipe_from_url, name='recipe_from_url'),
                url(r'^(?P<recipeSlug>[-\w]+)/?$', views.getRecipe, name='getrecipe'),
                ]
