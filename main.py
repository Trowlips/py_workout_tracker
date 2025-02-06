import json
import os
import requests
from dotenv import load_dotenv
import datetime as dt

load_dotenv()

# NUTRI
nutri_id = os.getenv("NUTRI_APP_ID")
nutri_api_key = os.getenv("NUTRI_API_KEY")
nutri_base = os.getenv("NUTRI_BASE_ENDPOINT")

sheet_api = os.getenv("SPREADSHEET_ENDPOINT")
sheet_auth = os.getenv("SPREADSHEET_AUTHORIZATION")

nl_exercise_endpoint = f"{nutri_base}/v2/natural/exercise"

current_date = dt.datetime.now()
formatted_date = current_date.strftime("%d/%m/%Y")
formatted_time = current_date.strftime("%X")

user_query = input("Tell me which exercise you did: ")

nutri_headers = {
    "x-app-id": nutri_id,
    "x-app-key": nutri_api_key
}

nutri_json = {
    "query": user_query
}

nutri_response = requests.post(nl_exercise_endpoint,json=nutri_json, headers=nutri_headers)
nutri_response.raise_for_status()

nutri_data = nutri_response.json()["exercises"]
for data in nutri_data:
    exercise = data["name"]
    duration = data["duration_min"]
    calories = data["nf_calories"]

    sheet_json = {
        "workout": {
            "date": formatted_date,
            "time": formatted_time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }

    sheet_header = {
        "content-type": "application/json",
        "Authorization": sheet_auth
    }

    sheet_response = requests.post(sheet_api, json=sheet_json, headers=sheet_header)
    sheet_response.raise_for_status()
    print(json.dumps(sheet_response.json(), indent=4))