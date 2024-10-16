import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
from datetime import datetime

# Constants
API_KEY = 'bc186ccd52f2d2031a06cf83bba23afc'  # Replace with your OpenWeatherMap API key
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
ICON_URL = "http://openweathermap.org/img/wn/"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Weather App")
        self.root.geometry("500x600")
        self.root.configure(bg='#e6f2ff')

        # Default values
        self.units = 'metric'  # Default to Celsius
        self.location = tk.StringVar()

        # Create the UI
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title = tk.Label(self.root, text="🌤️ Weather App 🌧️", font=("Arial", 20, "bold"), bg='#e6f2ff', fg='#003366')
        title.pack(pady=15)

        # Location Input
        location_frame = tk.Frame(self.root, bg='#f0f8ff')
        location_frame.pack(pady=10)
        tk.Label(location_frame, text="Enter Location:", font=("Arial", 10, "bold"), bg='#f0f8ff', fg='#333333').grid(row=0, column=0, padx=5)
        tk.Entry(location_frame, textvariable=self.location, font=("Arial", 10), width=30).grid(row=0, column=1)

        # Buttons for actions
        self.search_button = tk.Button(self.root, text="Search", command=self.get_weather, bg='#4682b4', fg='#ffffff', font=("Arial", 10, "bold"), width=20)
        self.search_button.pack(pady=10)

        # Temperature Unit Toggle
        self.unit_toggle = tk.Button(self.root, text="Switch to °F", command=self.toggle_units, bg='#ff8c00', fg='#ffffff', font=("Arial", 10, "bold"), width=20)
        self.unit_toggle.pack(pady=10)

        # Weather Information Frame
        self.weather_frame = tk.Frame(self.root, bg='#e6f2ff')
        self.weather_frame.pack(pady=20)

        # Weather icon and main weather info in a grid for alignment
        self.weather_icon = tk.Label(self.weather_frame, bg='#e6f2ff')
        self.weather_icon.grid(row=0, column=0, rowspan=2, padx=10)

        self.weather_info = tk.Label(self.weather_frame, text="", font=("Arial", 12, "bold"), bg='#e6f2ff', fg='#003366')
        self.weather_info.grid(row=0, column=1, sticky="w")  # Align left

        # Additional Weather Info Button
        self.extended_info_button = tk.Button(self.root, text="Extended Weather Info", command=self.open_extended_info, bg='#3cb371', fg='#ffffff', font=("Arial", 10, "bold"), width=30)
        self.extended_info_button.pack(pady=10)

    def get_weather(self):
        location = self.location.get()
        if not location:
            messagebox.showerror("Error", "Please enter a valid location!")
            return

        # Fetch weather data from API
        params = {
            'q': location,
            'appid': API_KEY,
            'units': self.units
        }

        try:
            response = requests.get(WEATHER_URL, params=params)
            data = response.json()
            if data['cod'] != 200:
                messagebox.showerror("Error", data.get("message", "Failed to get weather data"))
                return

            self.display_weather(data)

        except requests.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_weather(self, data):
        # Parse weather data
        city = data.get('name', '')
        country = data.get('sys', {}).get('country', '')
        temp = data.get('main', {}).get('temp', '')
        weather_description = data.get('weather', [])[0].get('description', '').capitalize()
        wind_speed = data.get('wind', {}).get('speed', '')
        rain = data.get('rain', {}).get('1h', 0)  # Precipitation in the last hour

        # Set weather information
        self.weather_info.config(text=f"{city}, {country}\n{temp}° {'C' if self.units == 'metric' else 'F'} - {weather_description}\nWind: {wind_speed} m/s")

        # Set weather icon
        icon_code = data.get('weather', [])[0].get('icon', '')
        self.update_weather_icon(icon_code)

        # Store additional data for later use
        self.additional_data = {
            'humidity': data.get('main', {}).get('humidity', ''),
            'pressure': data.get('main', {}).get('pressure', ''),
            'sunrise': data.get('sys', {}).get('sunrise', ''),
            'sunset': data.get('sys', {}).get('sunset', ''),
            'rain': rain,
        }

    def update_weather_icon(self, icon_code):
        try:
            icon_url = f"{ICON_URL}{icon_code}@2x.png"
            response = requests.get(icon_url, stream=True)
            image = Image.open(response.raw).resize((100, 100))
            icon = ImageTk.PhotoImage(image)
            self.weather_icon.config(image=icon)
            self.weather_icon.image = icon
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load icon: {e}")

    def toggle_units(self):
        # Toggle between Celsius and Fahrenheit
        if self.units == 'metric':
            self.units = 'imperial'
            self.unit_toggle.config(text="Switch to °C")
        else:
            self.units = 'metric'
            self.unit_toggle.config(text="Switch to °F")
        # Refresh the weather data if already available
        if self.location.get():
            self.get_weather()

    def open_extended_info(self):
        # Create a new window for extended weather info
        extended_window = tk.Toplevel(self.root)
        extended_window.title("Extended Weather Info")
        extended_window.geometry("300x300")  # Adjust size for more info
        extended_window.configure(bg='#e6f2ff')

        # Parse additional data
        humidity = self.additional_data.get('humidity', 'N/A')
        pressure = self.additional_data.get('pressure', 'N/A')
        sunrise = datetime.fromtimestamp(self.additional_data.get('sunrise', 0)).strftime('%I:%M %p')
        sunset = datetime.fromtimestamp(self.additional_data.get('sunset', 0)).strftime('%I:%M %p')
        rain = self.additional_data.get('rain', 0)

        # Create labels for additional weather info
        tk.Label(extended_window, text=f"Humidity: {humidity}%", font=("Arial", 12), bg='#e6f2ff', fg='#333333').pack(pady=5)
        tk.Label(extended_window, text=f"Pressure: {pressure} hPa", font=("Arial", 12), bg='#e6f2ff', fg='#333333').pack(pady=5)
        tk.Label(extended_window, text=f"Sunrise: {sunrise}", font=("Arial", 12), bg='#e6f2ff', fg='#333333').pack(pady=5)
        tk.Label(extended_window, text=f"Sunset: {sunset}", font=("Arial", 12), bg='#e6f2ff', fg='#333333').pack(pady=5)
        tk.Label(extended_window, text=f"Rain: {rain} mm", font=("Arial", 12), bg='#e6f2ff', fg='#333333').pack(pady=5)

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()