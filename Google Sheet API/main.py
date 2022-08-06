import requests
from datetime import datetime as dt

# -------------------VALUES
GENDER = "Male"
WEIGHT_KG = 77
HEIGHT_CM = 180
AGE = 31
my_api_id = "api_id"
my_api_key = "api_key"
my_sheety_key = "sheety_key"
header_sheety = {
    "Authorization": "Bearer sheety_key"
}

# ----------------Nutritionix JSON Get
my_headers = {
    "x-app-id": my_api_id,
    "x-app-key": my_api_key,
    "Content-Type": "application/json"
}

exercise_end_point = "https://trackapi.nutritionix.com/v2/natural/exercise"
QUERY = str(input("Tel me, what did you do today?:  "))
params = {
    "query": QUERY,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
response = requests.post(url=exercise_end_point, json=params, headers=my_headers)
data = response.json()

# ----------------Read Sheety
# sheety_get_url = "https://api.sheety.co/40473cb9fd40e20b5deca19d5ddc0cc3/myWorkouts/workouts"
# response = requests.get(url=sheety_get_url, headers=header_sheety)
# print(response.json())


# -----------------Calculate Datetime
today = dt.today()
today_conf = today.strftime("%d/%m/%Y")
time_conf = today.strftime("%X")

# -----------------Add A Row to Sheety

sheety_post_url = "https://api.sheety.co/40473cb9fd40e20b5deca19d5ddc0cc3/myWorkouts/workouts"
for exercise in data["exercises"]:
    post_that = {
        "workout": {
            "date": today_conf,
            "time": time_conf,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    response = requests.post(url=sheety_post_url, json=post_that, headers=header_sheety)
