from django.db import models

class Ingredient(models.Model):
    # primary ingredient name e.g. bread flour
    primary_name = models.CharField(
                                    max_length = 20,
                                    verbose_name = 'Primary Name',
                                    )
    # csv of alternate names for ingredient e.g. 00 flour,strong flour
    alternate_names = models.CharField(
                                        max_length = 200,
                                        verbose_name = 'Alternate Names',
                                        blank = True,
                                        null = True
                                        )

    def __str__(self):
        return self.primary_name

    def list_alternate_names(self):
        #split csv of alternate names over , to return list of alternate names
        return self.alternate_names.split(',')

class Recipe(models.Model):
    #recipe title
    title = models.CharField(max_length = 40)
    #recipe source (e.g. NYT, Bon Appetit)
    source = models.CharField(max_length = 100)
    #contributor (user who uploaded) eventually this will link to user model, now just ask for name when submitting
    contributor = models.CharField(max_length = 100)
    #number of people recipe serves
    serves = models.PositiveSmallIntegerField()
    #time to prepare recipe in minutes
    prep_time = models.PositiveIntegerField()
    #time to cook recipe in minutes
    cook_time = models.PositiveIntegerField()
    #list of ingredients (many to many field)
    ingredients = models.ManyToManyField(Ingredient)
    #csv with ingredient primary name and quantity deliminated as follows: flour,100g;water,50g;salt,1tsp
    ingredient_list = models.CharField(max_length = 500)
    #instruction list - determine format later
    instructions = models.TextField()
    #meal type (choices: breakfast, lunch, dinner, dessert, snack)
    MEAL_TYPE_CHOICES = (
        ('BRE', 'BREAKFAST'),
        ('LUN', 'LUNCH'),
        ('DIN', 'DINNER'),
        ('DES', 'DESSERT'),
        ('SNA', 'SNACK')
    )
    meal_type = models.CharField(max_length = 3, choices = MEAL_TYPE_CHOICES, default = 'DIN')
    #dish type (choices: vegetable, meat, carbohydrate, all-in-one, other)
    DISH_TYPE_CHOICES = (
        ('VEG', 'VEGETABLE'),
        ('MEA', 'MEAT'),
        ('CAR', 'CARBOHYDRATE'),
        ('ALL', 'ALL-IN-ONE'),
        ('OTH', 'OTHER')
    )
    dish_type = models.CharField(max_length = 3, choices = DISH_TYPE_CHOICES, default = 'VEG')
    #flavor profile helps create meals that go together
