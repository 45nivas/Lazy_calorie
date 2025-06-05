from django.test import TestCase
from .models import FoodItem, MealLog

class FoodItemModelTest(TestCase):
    def setUp(self):
        self.food_item = FoodItem.objects.create(
            name="Apple",
            calories=95,
            protein=0.5,
            carbs=25,
            fat=0.3
        )

    def test_food_item_creation(self):
        self.assertEqual(self.food_item.name, "Apple")
        self.assertEqual(self.food_item.calories, 95)
        self.assertEqual(self.food_item.protein, 0.5)
        self.assertEqual(self.food_item.carbs, 25)
        self.assertEqual(self.food_item.fat, 0.3)

class MealLogModelTest(TestCase):
    def setUp(self):
        self.food_item = FoodItem.objects.create(
            name="Banana",
            calories=105,
            protein=1.3,
            carbs=27,
            fat=0.3
        )
        self.meal_log = MealLog.objects.create(
            food_item=self.food_item,
            quantity=2
        )

    def test_meal_log_creation(self):
        self.assertEqual(self.meal_log.food_item.name, "Banana")
        self.assertEqual(self.meal_log.quantity, 2)
        self.assertEqual(self.meal_log.total_calories(), 210)  # 105 * 2

    def test_meal_log_str(self):
        self.assertEqual(str(self.meal_log), "2 x Banana")