from django.shortcuts import render
from .forms import RecipeForm, UrlRecipeForm
from . import scrape_nyt as scrape
from .models import Recipe, RecipeIngredient, Unit, Ingredient
from django.template.defaultfilters import slugify
import itertools
from nltk.stem.porter import PorterStemmer
import string

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

def jaccard_similarity(list1, list2):
    overlap_set = set(list1+list2)
    nunique = len(overlap_set)
    n1 = len(set(list1))
    n2 = len(set(list2))

    w1 = 1.0
    w2 = 1.0
    for item in overlap_set:
        if ((item in list1) and (item in list2)):
            w1 = w1*(1.0 - list1.index(item) / float(len(list1)))
            w2 = w2*(1.0 - list2.index(item) / float(len(list1)))

    noverlap = (n1+n2-nunique)
    return w1*w2*float(noverlap) / float(nunique)

def match_ingredients(ing_raw, ingredient_set):
    max_score = 0.0
    stemmer = PorterStemmer()
    for c in string.punctuation:
        raw_ingredient= ing_raw.replace(c,"")
    ing_raw_list = raw_ingredient.lower().split(' ')
    ing_raw_stem = [stemmer.stem(word) for word in ing_raw_list]
    for ingredient in ingredient_set:
        ing_std_list = ingredient.primary_name.split(' ')
        ing_std_stem = [stemmer.stem(word) for word in ing_std_list]
        all_scores = []
        all_scores.append(jaccard_similarity(ing_raw_stem, ing_std_stem))
        alt_names = ingredient.alternate_names
        if not alt_names: # in case alternate_names field is empty
            alt_names = ''
        for alt in alt_names.split(','):
            alt_std_list = alt.strip().split(' ')
            alt_std_stem = [stemmer.stem(word) for word in alt_std_list]
            all_scores.append(jaccard_similarity(ing_raw_stem, alt_std_stem))
        if (max(all_scores) > max_score):
            ingredient_match = ingredient
            max_score = max(all_scores)
    return ingredient_match



def extract_ingredient_info(ing, unit_set, ingredient_set):
    unit_match = unit_set.get(unit_name='count')
    ingredient_match = ingredient_set.get(primary_name='unmatched')
    # Iterate through units and see if any of them are in our string
    for u in unit_set:
        if u.unit_name in ing.lower():
            unit_match = u
            break
    # Iterate through ingredients and see if any of them are in our string
    ingredient_match = match_ingredients(ing, ingredient_set)
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
            unit_set = Unit.objects.all()
            ingredient_set = Ingredient.objects.all()
            for index, (ing, quant) in enumerate(zip(recipe_info.ingredient_names, recipe_info.ingredient_quantities)):
                #match ingredient
                #ing_match and unit_match will be objects from units / ingredients sets
                #or else None if no match is found
                unit_match, ing_match = extract_ingredient_info(ing, unit_set, ingredient_set)

                #find quantity
                # quantity = None
                # try:
                #     quantity = float(quant)
                # except:
                #     quantity = -1
                # #create instance (include index)
                # if not quant:
                #     quant = ''

                recipe_ingredient_row = RecipeIngredient.objects.create(
                        recipe_text = ing,
                        index = index,
                        matched_ingredient = ing_match,
                        unit = unit_match,
                        # ammount_text = quant,
                        ammount = quant,
                        associated_recipe_slug = recipe_slug
                    )
                #add ingredient to recipe
                recipe_instance.ingredient_list.add(recipe_ingredient_row)  #adds the ingredient object to the recipe. this relationship is many to one
            return render(request, 'recipes/success.html')
    else:
        form = UrlRecipeForm()
        return render(request, 'recipes/recipe_edit.html', {'form': form})
