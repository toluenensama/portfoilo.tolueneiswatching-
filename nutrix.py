import datetime as dt
from dotenv import find_dotenv,load_dotenv
import os
import requests
dotenv_path = find_dotenv()
GENDER = "M"
AGE = 22
HEIGHT = 180
WEIGHT = 70
EMAIL = "toludaniel.ojo@gmail.com"
NAME = "Tolu Ojo"

now_time = dt.datetime.now()
time_now = now_time.strftime("%H:%M:%S")
print(time_now)

today_date = now_time.strftime("%d/%m/%Y")
# print(f"{time_now} ## {today_date}")

api = "	https://trackapi.nutritionix.com"
API_ID = os.getenv("API_ID")
API_KEY = os.getenv("API_KEY")
headers = {
    "x-app-id" : API_ID,
    "x-app-key" : API_KEY

}
exercise_endpoint = f"{api}/v2/natural/exercise"


query =str(input("Tell me which exercise you did: "))
PARAMETERS = {
    "query": query,
    "height_cm" : HEIGHT,
    "weight_kg" : WEIGHT,
    "age" : AGE,


}

update = {
    "date" : today_date,

}
my_pass =os.getenv("MY_PASS")
headers1 = {
    "Authorization": f"Basic {my_pass}"
}


sheety_url = str(os.getenv("SHEETY_ENDPOINT"))
print(sheety_url)
print(API_KEY)
response = requests.post(url=exercise_endpoint,json=PARAMETERS,headers=headers)
# response = requests.get(url=sheety_url)
results = response.json()
print(response.text)
for exercise in results["exercises"]:
    sheet_inputs ={
    "workout" : {
        "date" :str(today_date),
        "time" : str(time_now),
        "exercise" : exercise["name"].title(),
        "duration" : exercise["duration_min"],
        "calories" : exercise["nf_calories"]
        }
    }
    sheet_response = requests.post(url=sheety_url,json=sheet_inputs,headers=headers1)
    print(sheet_response.text)

