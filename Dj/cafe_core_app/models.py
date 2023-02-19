from django.db import models


class MealType(models.TextChoices):
    HOT_MEALS = 'Горячие блюда'
    DRINKS = 'Напитки'
    DESSERT = 'Десерты'
    NO_TYPE = 'NO_TYPE'


class MealCategory(models.Model):
    meal_type = models.CharField(
        max_length=30,
        choices=MealType.choices,
        default=MealType.NO_TYPE
    )

    def __str__(self):
        return self.meal_type


class MealPhoto(models.Model):
    path = models.TextField()
    title = models.DateTimeField()

    def __str__(self):
        return self.path


class Meal(models.Model):
    name = models.CharField('Название блюда', max_length=100)
    detail = models.TextField('Описание блюда', unique=True)
    price = models.IntegerField('Стоимость блюда')
    size = models.IntegerField('Порция')
    category = models.ForeignKey(MealCategory, on_delete=models.DO_NOTHING)
    photo = models.ManyToManyField(MealPhoto, default=None, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

    def get_category_meal_type(self):
        return self.category.meal_type if self.category else None


class MealClick(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.DO_NOTHING)
    click_date = models.DateField('Дата клика')

    def get_meal(self):
        return self.meal.name if self.meal else None





