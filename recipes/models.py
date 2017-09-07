from django.db import models

class IngredientCategory(models.Model):
    name = models.CharField(max_length = 50, verbose_name = 'Ingredient Category', unique = True)
    class Meta:
        verbose_name_plural = 'Ingredient Categories'

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    # primary ingredient name e.g. bread flour
    primary_name = models.CharField(
                                    max_length = 20,
                                    verbose_name = 'Primary Name',
                                    unique = True
                                    )
    alternate_names = models.CharField(max_length = 500, verbose_name = 'Alternate Names', blank = True, null = True)
    category = models.ManyToManyField(IngredientCategory)

    def __str__(self):
        return self.primary_name

class Unit(models.Model):
    UNIT_TYPE_CHOICES = (
                            ('WGT', 'WEIGHT'),
                            ('VOL', 'VOLUME'),
                            ('CNT', 'COUNT')
                        )
    unit_type = models.CharField(max_length = 3, choices = UNIT_TYPE_CHOICES, default = 'CNT')

    unit_name = models.CharField(max_length = 20)
    unit_name_plural = models.CharField(max_length = 21)
    unit_abbreviation = models.CharField(max_length = 5)
    unit_abbreviation_plural = models.CharField(max_length = 6)

    # def alternate_forms(self, abbreviation = True, plural = True):
    #     units_all_forms = [
    #                         ['LBS', 'POUND', 'POUNDS', 'LB', 'LBS'],
    #                         ['KGS', 'KILOGRAM', 'KILOGRAMS', 'KG', 'KG'],
    #                         ['GRA', 'GRAM', 'GRAMS', 'G', 'G'],
    #                         ['OZS', 'OUNCE', 'OUNCES', 'OZ', 'OZ'],
    #                         ['LIT', 'LITER', 'LITERS', 'L', 'L'],
    #                         ['MLS', 'MILILITER', 'MILILITERS', 'ML', 'ML'],
    #                         ['CUP', 'CUP', 'CUPS', 'C', 'C'],
    #                         ['TSP', 'TEASPOON', 'TEASPOONS', 'TSP', 'TSP'],
    #                         ['TBS', 'TABLESPOON', 'TABLESPOONS', 'TBSP', 'TBSP'],
    #                         ['PIN', 'PINT', 'PINTS', 'PT', 'PT'],
    #                         ['QRT', 'QUART', 'QUARTS', 'QT', 'QT'],
    #                         ['GAL', 'GALLON', 'GALLONS', 'GAL', 'GAL'],
    #                         ['FLZ', 'FLUID OUNCE', 'FLUID OUNCES', 'FL OZ', 'FL OZ'],
    #                         ['PCH', 'PINCH', 'PINCHES', 'PINCH', 'PINCHES'],
    #                         ['DSH', 'DASH', 'DASHES', 'DASH', 'DASHES'],
    #                         ['CNT', 'COUNT', 'COUNT', 'COUNT', 'COUNT']
    #                     ]
    #     for unit_forms in units_all_forms:
    #         if self.unit == unit_forms[0]:
    #             if not abbreviation and not plural:
    #                 return unit_forms[1]
    #             else if not abbreviation and plural:
    #                 return unit_forms[2]
    #             else if abbreviation and not plural:
    #                 return unit_forms[3]
    #             else if abbreviation and plural:
    #                 return unit_forms[4]

    def __str__(self):
        return self.unit_name

class RecipeIngredient(models.Model):
    recipe_text = models.CharField(max_length = 100)
    index = models.IntegerField(verbose_name = 'Ingredient Index')
    matched_ingredient = models.ForeignKey(Ingredient)
    unit = models.ForeignKey(Unit, blank = True, null = True)
    ammount = models.DecimalField(max_digits = 14, decimal_places = 10)
    # ammount_text = models.CharField(max_length = 150)
    associated_recipe_slug = models.CharField(max_length = 40)

    def __str__(self):
        return self.recipe_text

class Recipe(models.Model):
    #recipe title and  derived url slug
    title = models.CharField(max_length = 40, unique = True)
    slug = models.SlugField(max_length = 40, unique = True)
    prepopulated_fields = {'slug': ('title', ),}
    #recipe source (e.g. NYT, Bon Appetit)
    source = models.CharField(max_length = 100)
    #recipe source url, note this is not required since some recipes will not have a source url
    source_url = models.CharField(max_length = 100, blank = True, null = True)
    #contributor (user who uploaded) eventually this will link to user model, now just ask for name when submitting
    contributor = models.CharField(max_length = 100)
    #recipe yeild
    serves = models.PositiveIntegerField(blank = True, null = True)
    #What is the recipe output. This may be how many brownies a recipe makes
    yeild = models.CharField(max_length=50)
    #time to prepare recipe in minutes
    prep_time = models.PositiveIntegerField(blank = True, null = True)
    #time to cook recipe in minutes
    cook_time = models.PositiveIntegerField(blank = True, null = True)
    #list of ingredients (many to many field)
    ingredient_list = models.ManyToManyField(RecipeIngredient)
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

    def __str__(self):
        return self.title

    def instructions_as_list(self):
        return self.instructions.split(';;')
