import requests
city = input("Enter city name:")
url = f"https://wttr.in//{city}?format=j1"
response = requests.get(url)
data = response.json()
temprature = data["current_condition"][0]["temp_C"]
print(f"current temperature in {city} is {temprature}°C")