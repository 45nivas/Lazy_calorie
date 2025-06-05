from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import FoodItem, MealLog
from .serializers import FoodItemSerializer, MealLogSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import render
from .models import FoodItem, MealLog
import json
import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_ollama_for_foods(text):
    prompt = (
        f"You are a nutrition expert. Parse this meal: '{text}'. "
        "For each food, estimate the total calories, protein, carbs, and fat for the given quantity and unit. "
        "Return ONLY a JSON array, one object per food, with keys: food, quantity, unit, calories, protein, carbs, fat. "
        "Example: [{\"food\": \"chicken\", \"quantity\": 100, \"unit\": \"g\", \"calories\": 239, \"protein\": 27, \"carbs\": 0, \"fat\": 14}]"
    )
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=20)
    resp.raise_for_status()
    print("Ollama RAW response:", resp.text)
    try:
        # Parse the top-level JSON object
        resp_json = resp.json()
        response_text = resp_json.get("response", "")
        # Extract the JSON array from the response string
        match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if match:
            foods = json.loads(match.group())
        else:
            foods = []
    except Exception as e:
        print("JSON decode error:", e)
        foods = []
    print("Ollama foods:", foods)
    return foods

def index(request):
    return render(request, "tracker/index.html")

@csrf_exempt
def log_meal_from_voice(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)
    try:
        data = json.loads(request.body)
        transcribed_text = data.get("text", "")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    if not transcribed_text:
        return JsonResponse({"error": "No transcribed text provided"}, status=400)

    # Use Ollama to parse foods and macros
    try:
        foods = query_ollama_for_foods(transcribed_text)
    except Exception as e:
        return JsonResponse({"error": f"Ollama error: {str(e)}"}, status=500)
    if not isinstance(foods, list) or not foods:
        return JsonResponse({"error": "Could not parse foods from input"}, status=400)

    results = []
    for food_obj in foods:
        if not isinstance(food_obj, dict):
            continue
        food = food_obj.get("food")
        quantity = float(food_obj.get("quantity") or 1)
        unit = food_obj.get("unit") or ""
        calories = float(food_obj.get("calories", 0))
        protein = float(food_obj.get("protein", 0))
        carbs = float(food_obj.get("carbs", 0))
        fat = float(food_obj.get("fat", 0))
        if not food:
            continue

        # Save or update FoodItem (for reference)
        food_item, _ = FoodItem.objects.get_or_create(
            name=food,
            defaults={
                "calories_per_100g": calories,
                "protein": protein,
                "carbs": carbs,
                "fat": fat,
            }
        )
        # Always update macros
        food_item.calories_per_100g = calories
        food_item.protein = protein
        food_item.carbs = carbs
        food_item.fat = fat
        food_item.save()

        # Save MealLog with actual macros for this meal
        MealLog.objects.create(
            food_item=food_item,
            quantity=quantity,
            unit=unit,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            date=timezone.now().date()
        )
        results.append({
            "food": food,
            "quantity": quantity,
            "unit": unit,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
        })

    # Aggregate today's macros (sum actual values)
    today = timezone.now().date()
    logs = MealLog.objects.filter(date=today)
    total_calories = sum(log.calories for log in logs)
    total_protein = sum(log.protein for log in logs)
    total_carbs = sum(log.carbs for log in logs)
    total_fats = sum(log.fat for log in logs)

    return JsonResponse({
        "logged": results,
        "date": str(today),
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fats": total_fats,
    })

@csrf_exempt
def get_daily_summary(request):
    if request.method == "GET":
        today = timezone.now().date()
        logs = MealLog.objects.filter(date=today)
        total_calories = sum(log.calories for log in logs)
        total_protein = sum(log.protein for log in logs)
        total_carbs = sum(log.carbs for log in logs)
        total_fats = sum(log.fat for log in logs)
        return JsonResponse({
            "date": str(today),
            "total_calories": total_calories,
            "total_protein": total_protein,
            "total_carbs": total_carbs,
            "total_fats": total_fats,
        })
    return JsonResponse({"error": "GET required"}, status=400)

@csrf_exempt
def get_daily_meals(request):
    if request.method == "GET":
        today = timezone.now().date()
        logs = MealLog.objects.filter(date=today)
        meals = []
        for log in logs:
            meals.append({
                "food": log.food_item.name,
                "quantity": log.quantity,
                "unit": log.unit,
                "calories": log.calories,
                "protein": log.protein,
                "carbs": log.carbs,
                "fat": log.fat,
            })
        return JsonResponse({"meals": meals})
    return JsonResponse({"error": "GET required"}, status=400)