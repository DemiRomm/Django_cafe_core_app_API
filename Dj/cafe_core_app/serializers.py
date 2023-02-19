from rest_framework import serializers
from .models import Meal, MealCategory, MealClick, MealPhoto

class MenuSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    photo = serializers.StringRelatedField(many=True, read_only=False)

    class Meta:
        model = Meal
        fields = [
            'id',
            'name',
            'category',
            'detail',
            'price',
            'size',
            'photo'
        ]

    def get_category(self, instance: Meal):
        return instance.category.meal_type if instance.category is not None else None


class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealCategory
        fields = ['meal_type']

class MealPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPhoto
        fields = ['path']

class NewMealSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_meal_type') # переопределяет поле в модели с названием этого поля (category) В данном случае, она вызывает ф-ю get_category_meal_type в модели MEal и получает объект
    class Meta:
        model = Meal
        fields = [
            'id',
            'name',
            'category',
            'detail',
            'price',
            'size',
            'photo'
        ]

    def update(self, instance, validated_data):
        category = validated_data.pop('get_category_meal_type', instance.category)
        instance = super().update(instance, validated_data)
        instance.category = category
        instance.save()
        return instance

    def validate_category(self, value):
        category = MealCategory.objects.get(meal_type=value)
        return category

    def create(self, validated_data):
        cat = validated_data.pop('get_category_meal_type')
        obj = Meal.objects.create(**validated_data, category=cat)
        return obj


class MealClickSerializer(serializers.ModelSerializer):
    meal = serializers.SerializerMethodField()

    class Meta:
        model = MealClick
        fields = [
            'id',
            'meal',
            'click_date',
        ]

    def get_meal(self, instance: MealClick):
        return instance.meal.name if instance.meal else None


