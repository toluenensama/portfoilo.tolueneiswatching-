import requests
GENDER = "M"
AGE = 22
HEIGHT = 180
WEIGHT = 70


api = "	https://trackapi.nutritionix.com"
API_ID = "c09ffbc2"
API_KEY = "a174a3e897f6d2e2e7d9a843eff9bd0d"
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

response = requests.post(url=exercise_endpoint,json=PARAMETERS,headers=headers)
results = response.json()
print(results)
