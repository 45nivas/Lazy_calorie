from rest_framework import serializers
from .models import FoodItem, MealLog, DailySummary

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'calories', 'protein', 'carbs', 'fat']

class MealLogSerializer(serializers.ModelSerializer):
    food_items = FoodItemSerializer(many=True)

    class Meta:
        model = MealLog
        fields = ['id', 'date', 'meal_type', 'food_items']

class DailySummarySerializer(serializers.ModelSerializer):
    meal_logs = MealLogSerializer(many=True)

    class Meta:
        model = DailySummary
        fields = ['date', 'total_calories', 'total_protein', 'total_carbs', 'total_fat', 'meal_logs']