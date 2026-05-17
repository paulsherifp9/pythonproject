import tkinter as tk
import requests


def get_weather():

    city = city_entry.get()

    url = f"https://wttr.in/{city}?format=j1"

    response = requests.get(url)

    data = response.json()

    temperature = data["current_condition"][0]["temp_C"]

    result_label.config(
        text=f"Current temperature in {city} is {temperature}°C"
    )


window = tk.Tk()

window.title("Weather App")

window.geometry("400x250")


title_label = tk.Label(
    window,
    text="Weather App",
    font=("Arial", 20)
)

title_label.pack(pady=10)


city_entry = tk.Entry(
    window,
    font=("Arial", 14)
)

city_entry.pack(pady=10)


search_button = tk.Button(
    window,
    text="Get Weather",
    font=("Arial", 14),
    command=get_weather
)

search_button.pack(pady=10)


result_label = tk.Label(
    window,
    text="",
    font=("Arial", 14)
)

result_label.pack(pady=20)


window.mainloop()