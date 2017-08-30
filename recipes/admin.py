from django.contrib import admin
from recipes.models import Ingredient, Recipe, Unit, RecipeIngredient, IngredientCategory

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Unit)
admin.site.register(RecipeIngredient)
admin.site.register(IngredientCategory)
