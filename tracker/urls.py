from django.urls import path
from .views import log_meal_from_voice, get_daily_summary, index, get_daily_meals

urlpatterns = [
    path('', index, name='home'),
    path('voice-log/', log_meal_from_voice, name='voice_log'),
    path('get-daily-summary/', get_daily_summary, name='get_daily_summary'),
    path('get-daily-meals/', get_daily_meals, name='get_daily_meals'),
]