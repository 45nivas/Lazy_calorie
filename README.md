# Voice-Powered Calorie and Macro Tracker

This project is a voice-powered calorie and macro tracker that replicates features similar to MyFitnessPal. It allows users to log food entries and calculate daily macro totals using voice commands.

## Features

- Voice recognition for logging food entries
- REST API for managing food items and meal logs
- Daily macro tracking and summary
- User-friendly interface for tracking calories and macros

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd voice_calorie_tracker
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

5. **Run database migrations:**
   ```
   python manage.py migrate
   ```

6. **Start the development server:**
   ```
   python manage.py runserver
   ```

## Usage

- Access the API endpoints to log food entries and retrieve daily macro totals.
- Use voice commands to interact with the application for a seamless experience.

## Requirements

- Python 3.x
- Django
- Additional libraries for voice recognition and data processing (listed in `requirements.txt`)

## License

This project is licensed under the MIT License. See the LICENSE file for more details.