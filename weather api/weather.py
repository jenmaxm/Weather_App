import requests
from tkinter import *
from PIL import ImageTk, Image
import io

# Initialize window
window = Tk()
window.title("Weather App")
window.geometry("300x500")

# OpenWeather API details
API_KEY = "6642afdb065c2149b53a5499f6c08f47"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# UI Elements
Label(window, text="Enter City Name:").pack(pady=10)
city_entry = Entry(window, width=20, bg="black", fg="white")
city_entry.pack(pady=5)

weather_label = Label(window, text="", font=("Arial", 12))
weather_label.pack(pady=5)

temp_label = Label(window, text="", font=("Arial", 12))
temp_label.pack(pady=5)

icon_label = Label(window)
icon_label.pack(pady=10)

# Function to fetch weather data
def get_weather():
    city = city_entry.get().strip()
    if not city:
        weather_label.config(text="Please enter a city name.", fg="red")
        return

    request_url = f"{BASE_URL}?appid={API_KEY}&q={city}&units=metric"
    
    try:
        response = requests.get(request_url)
        data = response.json()

        if response.status_code == 200:
            weather = data["weather"][0]["description"].capitalize()
            temperature = round(data["main"]["temp"], 1)

            weather_label.config(text=f"Weather in {city}: {weather}", fg="black")
            temp_label.config(text=f"Temperature: {temperature}°C", fg="black")

            # Load and display the weather icon
            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            icon_response = requests.get(icon_url)
            icon_img = Image.open(io.BytesIO(icon_response.content))
            icon_img = icon_img.resize((80, 80))  # Resize the image
            icon_photo = ImageTk.PhotoImage(icon_img)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo

        else:
            weather_label.config(text="City not found. Try again.", fg="red")
            temp_label.config(text="")
            icon_label.config(image="")

    except requests.exceptions.RequestException:
        weather_label.config(text="Network error. Try again later.", fg="red")
        temp_label.config(text="")
        icon_label.config(image="")

# Function to reset labels
def clear_labels():
    weather_label.config(text="")
    temp_label.config(text="")
    icon_label.config(image="")

# Buttons
Button(window, text="Search", width=10, command=get_weather).pack(pady=5)
Button(window, text="Reset", width=10, command=clear_labels).pack(pady=5)

window.mainloop()
