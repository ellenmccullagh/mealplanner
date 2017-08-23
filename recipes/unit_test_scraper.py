import scrape_nyt


def test1():
    url = 'https://cooking.nytimes.com/recipes/1014970-smoky-eggplant-soup'
    recipe = scrape_nyt.get_recipe(url)
    recipe.print_recipe()

def test2():
    url = 'https://cooking.nytimes.com/recipes/1016230-robertas-pizza-dough'
    recipe = scrape_nyt.get_recipe(url)
    recipe.print_recipe()



if __name__ == '__main__':
    test1()
    test2()
