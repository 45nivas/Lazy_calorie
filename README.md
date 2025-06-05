# Voice Calorie Tracker

A Django web app that lets you log your meals by voice or text and instantly get calorie and macro estimates using an LLM (Ollama). No static food database or external API is required—nutrition is estimated by the LLM for any food you enter.

---

## Features

- **Voice or Text Meal Logging:** Speak or type your meal (e.g., "2 boiled eggs and 100g oats").
- **LLM Nutrition Estimation:** Uses Ollama (running a local LLM like Mistral) to parse and estimate calories, protein, carbs, and fat for any food.
- **Daily Summary:** See your total calories, protein, carbs, and fat for the day.
- **Meal Table:** View all meals logged today, with the ability to delete entries.
- **Modern UI:** Responsive, clean interface with toast notifications.
- **No Static Dataset Needed:** Works for any food, even if not in a database.

---

## How It Works

1. **User logs a meal** (by voice or text) on the web interface.
2. **Frontend sends the meal text** to the Django backend via `/api/voice-log/`.
3. **Backend calls Ollama LLM** with a prompt to parse and estimate nutrition for each food in the meal.
4. **LLM returns a JSON array** with food, quantity, unit, calories, protein, carbs, and fat.
5. **Backend saves the meal** (and macros) to the database for daily summary and meal listing.
6. **Frontend updates** the summary and meal table in real time.

---

## Setup Instructions

### 1. Requirements

- Python 3.8+
- Django
- Django REST Framework
- Ollama running locally (with a model like `mistral` installed)
- Node.js (optional, for frontend development)

### 2. Install Python Dependencies

```bash
pip install django djangorestframework requests
```

### 3. Set Up Ollama

- [Download and install Ollama](https://ollama.com/download)
- Pull a model (e.g., mistral):
  ```bash
  ollama pull mistral
  ```
- Start Ollama (it runs at `http://localhost:11434` by default)

### 4. Run Django Server

```bash
python manage.py migrate
python manage.py runserver
```

### 5. Access the App

Open [http://localhost:8000/](http://localhost:8000/) in your browser.

---

## API Endpoints

- `POST /api/voice-log/`  
  Request: `{"text": "2 boiled eggs and 100g oats"}`  
  Response:  
  ```json
  {
    "logged": [
      {
        "food": "egg",
        "quantity": 2,
        "unit": "boiled",
        "calories": 136,
        "protein": 11,
        "carbs": 1.2,
        "fat": 9.6
      },
      {
        "food": "oats",
        "quantity": 100,
        "unit": "g",
        "calories": 389,
        "protein": 16.9,
        "carbs": 66.3,
        "fat": 6.9
      }
    ]
  }
  ```

- `GET /api/get-daily-summary/`  
  Returns today's total calories, protein, carbs, and fat.

- `GET /api/get-daily-meals/`  
  Returns all meals logged today.

- `POST /api/delete-meal/`  
  Deletes a meal by ID.

---

## How Nutrition Estimation Works

- The backend sends your meal text to Ollama with a prompt like:
  > "You are a nutrition expert. Parse this meal: '2 boiled eggs and 100g oats'. For each food, estimate the total calories, protein, carbs, and fat for the given quantity and unit. Return ONLY a JSON array..."
- Ollama LLM responds with a JSON array of foods and their estimated macros.
- The backend saves this data and returns it to the frontend.

---

## Notes

- **No static food database is needed.** The LLM estimates nutrition for any food, including uncommon or regional foods.
- **Accuracy depends on the LLM model** and its training data. For medical or critical use, always double-check values.
- **No external API keys required.** All estimation is local via Ollama.

---

## Troubleshooting

- If you see all zeros for macros, make sure your backend is using the LLM for nutrition estimation and not falling back to static data.
- Ensure Ollama is running and accessible at `http://localhost:11434`.
- Check your browser console and Django logs for errors.

---

## Credits

- Built with Django, Ollama, and Mistral LLM.
- Inspired by MyFitnessPal, but fully private and local.

---