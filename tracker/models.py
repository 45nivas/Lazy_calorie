from django.db import models
from django.utils import timezone

class FoodItem(models.Model):
    name = models.CharField(max_length=200, unique=True)
    calories_per_100g = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return self.name


class MealLog(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=32, blank=True, default="")
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.food_item.name} on {self.date}"


class DailySummary(models.Model):
    date = models.DateField(unique=True)
    total_calories = models.PositiveIntegerField(default=0)
    total_protein = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_carbohydrates = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_fats = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Summary for {self.date}"

# Example of creating a MealLog entry
def create_meal_log(food_item, quantity):
    calories = (food_item.calories_per_100g * quantity) / 100
    protein = (food_item.protein * quantity) / 100
    carbs = (food_item.carbs * quantity) / 100
    fat = (food_item.fat * quantity) / 100

    MealLog.objects.create(
        food_item=food_item,
        quantity=quantity,
        date=timezone.now().date()
    )
