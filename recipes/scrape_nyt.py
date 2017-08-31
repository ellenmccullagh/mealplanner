import requests
from bs4 import BeautifulSoup
import re


class NYT_recipe:
    def __init__(self, url):
        self.url = url
        self.source = 'NYT recipes'
    def add_title(self, title):
        self.title = title
    def add_ingredients(self, ingredient_names, quantities):
        self.ingredient_names = ingredient_names
        self.ingredient_quantities = quantities
    def add_description(self, description):
        self.description = description
    def add_difficulty(self, difficulty):
        self.difficulty = difficulty
    def add_steps(self, steps):
        self.steps = steps
    def add_tags(self, tags):
        self.tags = tags
    def add_cooktime(self, cook_time):
        self.cook_time = cook_time
    def add_yield(self, recipe_yield):
        self.recipe_yield = recipe_yield
    def add_rating(self, nrating, nstars):
        self.num_ratings = nrating
        self.num_stars = nstars
    def print_recipe(self):
        print(self.url)
        print(self.title)
        print('Tags:')
        for tag in self.tags:
            print(tag)
        print('Yield: %s'%self.recipe_yield)
        print('Cook time: %s'%self.cook_time)
        for ing, quant in zip(self.ingredient_names, self.ingredient_quantities):
            print('%s %s'%(quant, ing))
        for i, step in enumerate(self.steps):
            print('Step %i:'%(i+1))
            print(step)
    def get_recipe_string(self):
        str_tot = self.title + ' ' + self.description
        for tag in self.tags:
            str_tot = str_tot + ' ' + tag
        for ing in self.ingredient_names:
            str_tot = str_tot + ' ' + ing
        return str_tot



def get_quantity_float(quantity):
    quantity = quantity.replace('½', '0.5').replace('¼', '0.25').replace('⅛', '0.125')
    try:
        return float(quantity)
    except Exception:
        pass
    if (re.match('[0-9]+ 0.[0-9]+', quantity) != None):
        print('here')
        quantity = re.sub('([0-9]+) 0.([0-9]+)', '\g<1>.\g<2>', quantity)
        print(quantity)
        try:
            return float(quantity)
        except Exception:
            pass
    for num in quantity.split(' '):
        if num.isnumeric():
            return float(num)
    return 0.0






# Scrapes the recipe at the given url
# and returns a recipe object

def get_recipe(url):
    # Assumes the URL is a valid NYT recipe URL
    recipe = NYT_recipe(url)
    # open the URL
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    if (soup == None):
        print('couldnt find recipe at:', url)
        return -1
    # First get the ingredient list (quantities and ingredients)
    ingredients = soup.findAll('ul', attrs={'class': 'recipe-ingredients'})
    quantities = []
    ingredient_names = []
    for ingred in ingredients:
        for row in ingred.findAll('li'):
            #print row.getText(separator=' ')

            tmp = row.find('span', attrs ={'class':'ingredient-name'})
            if (tmp != None):
                ingredient_names.append(tmp.getText(separator=' ').strip().replace('  ', ' '))
            tmp = row.find('span', attrs={'class': 'quantity'})
            if (tmp != None):
                quantity = tmp.getText(separator=' ').strip()
                quantities.append(get_quantity_float(quantity))
    recipe.add_ingredients(ingredient_names, quantities)
    # Next get the recipe steps
    steps = soup.find('ol', attrs={'class': 'recipe-steps'})
    recipe_steps = []
    for row in steps.findAll('li'):
        recipe_steps.append(row.getText())
    recipe.add_steps(recipe_steps)
    # Check to see if there is a difficulty rating
    difficulty = soup.find('a', attrs={'class': 'kicker easy'})
    if (difficulty == None):
        difficulty = 'None'
    else:
        difficulty = difficulty.getText()
    recipe.add_difficulty(difficulty)
    # Get the recipe title, if there is one
    title = soup.find('h1', attrs={'class':'recipe-title title name'})
    if (title == None):
        title = 'None'
    else:
        title = title.getText().strip()
    recipe.add_title(title)
    # Get the cook time, if there is one
    time_check = soup.find('span', attrs={'class': 'recipe-yield-time-label recipe-time'})
    if (time_check == None):
        time = 'None'
    else:
        time = soup.find('ul', attrs={'class': "recipe-time-yield"})
        time = time.findAll('li')[-1].getText(separator=',').strip(',').split(',')[-1]
    recipe.add_cooktime(time)
    # Get the recipe yield if there is one
    recipe_yield = soup.find('span', attrs = {'itemprop':"recipeYield"})
    if (recipe_yield == None):
        recipe_yield = 'None'
    else:
        recipe_yield = recipe_yield.getText()
    recipe.add_yield(recipe_yield)
    # Get the description of the recipe
    topnote = soup.find('div', attrs={'class': 'topnote'})
    if (topnote == None):
        topnote=''
    else:
        topnote = topnote.find('p').getText().strip()
    recipe.add_description(topnote)
    # Get any recipe tags
    nutrition = soup.find('div', attrs={'class': 'tags-nutrition-container'})
    recipe_tags = []
    if (nutrition != None):
        for tags in nutrition.findAll('a'):
            recipe_tags.append(tags.getText())
    recipe.add_tags(recipe_tags)

    rv = soup.find('span', attrs={'itemprop': 'ratingValue'})
    if (rv == None):
        rating_value = 0
    else:
        rating_value = int(rv.getText())
    rc = soup.find('span', attrs={'itemprop': 'ratingCount'})
    if (rc == None):
        rating_count = 0
    else:
        rating_count = int(rc.getText())
    recipe.add_rating(rating_count, rating_value)


    return recipe
