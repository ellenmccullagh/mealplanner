from django.shortcuts import render
from .forms import RecipeForm, UrlRecipeForm
from . import scrape_nyt as scrape
from .models import Recipe, RecipeIngredient
from django.template.defaultfilters import slugify

# Create your views here.

def index(request):
    return render(request, 'recipes/index.html')

def recipe_new(request):
    form = RecipeForm()
    return render(request, 'recipes/recipe_edit.html', {'form': form})

def getRecipe(request, recipeSlug):
    # Get specified protocol
    recipe = Recipe.objects.filter(slug=recipeSlug)
    # ingredients = recipe.ingredient_list.all()
    # Display specified protocol
    return render(request, 'recipes/recipe.html', {'recipe':recipe})

def recipe_from_url(request):
    #get the url from the form.
    #scrape the data from the url
    #create a recipe object and add all information except the ingredients
    #match the ingredients to known ingredients
    #create ingredient objects and add to recipe object as they are created
    if request.method == 'POST':
        form = UrlRecipeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            contributor = form.cleaned_data['contributor']

            # scrape and get info
            recipe_info  = scrape.get_recipe(url)

            #create slug and ensure uniqueness
            recipe_slug = orig = slugify(recipe_info.title)
            for x in itertools.count(1):
                if not Recipe.objects.filter(slug=recipe_slug).exists():
                    break
                recipe_slug = '{}s-{}d'.format(orig, x)

            # create recipe instance
            recipe_instance = Recipe.objects.create(
                            title = recipe_info.title,
                            slug = recipe_slug,
                            source = recipe_info.source,
                            source_url = url,
                            contributor = contributor,
                            yeild = recipe_info.recipe_yield,
                            #prep_time = ,
                            #cook_time = recipe_info.cook_time,
                            #ingredients = ,
                            instructions = ';;'.join(recipe_info.steps)
                                                    )
            #create ingredient instances
            for ing in recipe_info.ingredients:
                #match ingredient
                #find quantity
                #match unit
                #create instance (include index)
                #add ing instance to recipe_instance
                break
            return render(request, 'recipes/success.html')
    else:
        form = UrlRecipeForm()
        return render(request, 'recipes/recipe_edit.html', {'form': form})
