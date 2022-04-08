import dotenv
import os
import requests
from datetime import datetime

# API consts
dotenv.load_dotenv()
NUTR_APP_ID = os.getenv('NUTRITIONIX_APP_ID')
NUTR_API_KEY = os.getenv('NUTRITIONIX_API_KEY')
SHEETY_API = os.getenv('SHEETY_API')
SHEETY_TOKEN = os.getenv('SHEETY_TOKEN')

# ----- Nutritionix ----- #
def get_workout(query):
    nutr_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
    nutr_header = {
        'x-app-id': NUTR_APP_ID,
        'x-app-key': NUTR_API_KEY
    }
    nutr_params = {
        'query': query,
        'gender': 'male',
        'weight_kg': 93,
        'height_cm': 177,
        'age': 28
    }
    res_nutr = requests.post(nutr_endpoint, headers=nutr_header, json=nutr_params)
    res_nutr.raise_for_status()
    return res_nutr.json()

query = input("What exercise did you do?\t")
# demo_query = "ran 1 mile and swam 0.5 miles"
workout_data = get_workout(query=query)['exercises']


# ----- Save to Sheety ----- #
sheety_endpoint = f"https://api.sheety.co/{SHEETY_API}/workoutTracking/workouts"
sheety_header = {'Authorization': f"Bearer {SHEETY_TOKEN}"}


for workout in workout_data:
    body = {
        'workout': {
            'date': datetime.today().strftime("%m/%d/%Y"),
            'time': datetime.now().strftime("%H:%M:%S"),
            'exercise': workout['name'].title(),
            'duration': workout['duration_min'],
            'calories': workout['nf_calories']
            }
    }
    res_post = requests.post(sheety_endpoint, json=body, headers= sheety_header)
    res_post.raise_for_status()
    print(res_post.text)