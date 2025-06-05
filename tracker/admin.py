from django.contrib import admin
from .models import FoodItem, MealLog, DailySummary

admin.site.register(FoodItem)
admin.site.register(MealLog)
admin.site.register(DailySummary)