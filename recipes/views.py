from django.shortcuts import render
from .forms import RecipeForm, UrlRecipeForm
from . import scrape_nyt as scrape
from .models import Recipe, RecipeIngredient, Unit, Ingredient
from django.template.defaultfilters import slugify
import itertools

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

def extract_ingredient_info(ing, unit_set, ingredient_set):
    unit_match = unit_set.get(unit_name='count')
    ingredient_match = ingredient_set.get(primary_name='unmatched')
    # Iterate through units and see if any of them are in our string
    for u in unit_set:
        if u.unit_name in ing.lower():
            unit_match = u
            break
    # Iterate through ingredients and see if any of them are in our string
    for i in ingredient_set:
        if i.primary_name in ing.lower():
            # currently just finds the first ingredient match, then quits
            ingredient_match = i
            break
    return unit_match, ingredient_match


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
            index = 0
            for ing, quant in zip(recipe_info.ingredient_names, recipe_info.ingredient_quantities):
                #match ingredient
                #ing_match and unit_match will be objects from units / ingredients sets
                #or else None if no match is found
                unit_set = Unit.objects.all()
                ingredient_set = Ingredient.objects.all()
                unit_match, ing_match = extract_ingredient_info(ing, unit_set, ingredient_set)
                #find quantity
                quantity = None
                try:
                    quantity = int(quant)
                except ValueError:
                    quantity = -1
                #create instance (include index)
                recipe_ingredient_row = RecipeIngredient(
                        recipe_text = ing,
                        index = index,
                        matched_ingredient = ing_match,
                        unit = unit_match,
                        ammount_text = quant,
                        ammount = quantity, #not working now because quant is a string and ammount is a decimal
                        associated_recipe_slug = recipe_slug
                    )
                index += 1
                #add ingredient to recipe
                recipe_instance.ingredient_list.add(recipe_ingredient_row)  #adds the ingredient object to the recipe. this relationship is many to one
            return render(request, 'recipes/success.html')
    else:
        form = UrlRecipeForm()
        return render(request, 'recipes/recipe_edit.html', {'form': form})
