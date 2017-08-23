from django.shortcuts import render
from .forms import RecipeForm, UrlRecipeForm
from . import scrape_nyt as scrape
from .models import Recipe

# Create your views here.

def index(request):
    return render(request, 'recipes/index.html')

def recipe_new(request):
    form = RecipeForm()
    return render(request, 'recipes/recipe_edit.html', {'form': form})

def recipe_from_url(request):
    if request.method == 'POST':
        form = UrlRecipeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            contributor = form.cleaned_data['contributor']
            # scrape and get info
            recipe_info  = scrape.get_recipe(url)
            # reform ingredients into string
            ingredient_list = ''
            for i in range(len(recipe_info.ingredient_names)):
                entry = recipe_info.ingredient_names[i] + ';;' + recipe_info.ingredient_quantities[i]
                if i != len(recipe_info.ingredient_names):
                    entry += ';:;'
                ingredient_list += entry
            # store into django models
            recipe_instance = Recipe.objects.create(
                            title = recipe_info.title,
                            source = recipe_info.source,
                            source_url = url,
                            contributor = contributor,
                            yeild = recipe_info.recipe_yield,
                            #prep_time = ,
                            #cook_time = recipe_info.cook_time,
                            #ingredients = ,
                            ingredient_list = ingredient_list,
                            instructions = ';;'.join(recipe_info.steps)
                                                    )

            return render(request, 'recipes/success.html')
    else:
        form = UrlRecipeForm()
        return render(request, 'recipes/recipe_edit.html', {'form': form})
