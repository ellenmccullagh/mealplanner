from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
                    'title', 'source', 'contributor',
                    'serves', 'prep_time', 'cook_time',
                    'ingredient_list', 'ingredient_list', 'instructions',
                    'meal_type', 'dish_type'
                    )

class UrlRecipeForm(forms.Form):
    url = forms.CharField(label = 'url', max_length = 200)
    contributor = forms.CharField(label = 'your name', max_length = 50)
