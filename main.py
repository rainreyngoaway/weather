import json
from datetime import datetime

import requests
from rich import print
from rich.panel import Panel
from rich.console import Console


def main():

    Console().clear()
    LAT = 10.7460  # Replace with your Hometown Latitude
    LON = 124.7946  # Replace with your Hometown Longitude
    KEY = "d105f5f3d6c9ff8ba83d174c1a741f3d"

    API = "https://api.openweathermap.org/data/2.5/weather"
    URL = f"{API}?lat={LAT}&lon={LON}&units=metric&appid={KEY}"

    response = requests.get(URL).json()

    location = response.get("name")
    country = response.get("sys").get("country")

    date = get_formatted_datetime(response.get("dt"), "%Y-%m-%d %I:%S %p")
    sunrise = get_formatted_datetime(response.get("sys").get("sunrise"), "%I:%S %p")
    sunset = get_formatted_datetime(response.get("sys").get("sunset"), "%I:%S %p")

    weather = response.get("weather")[0].get("main")
    description = response.get("weather")[0].get("description").title()

    temperature = float(response.get("main").get("temp"))
    humidity = response.get("main").get("humidity")
    wind = response.get("wind").get("speed")

    color1 = "grey53"
    if "sky" in weather.lower():
        color1 = "yellow"
    elif "cloud" in weather.lower():
        color1 = "white"

    color2 = "blue"
    if 25 <= temperature < 30:
        color2 = "yellow"
    elif temperature >= 30:
        color2 = "red"


message = (
    f"[green underline]{location}, {country}[/green underline]\n"
    f"[white]{date}[/white]\n\n"
    f"[{color1}]{weather} [{color2}]{temperature}°C[/{color2}]\n"
    f"[italic][grey53]> {description}[/italic]\n\n"
    f"[white]Humidity: {humidity}%\n"
    f"Wind: {wind} km/h\n"
    f"Sunrise: {sunrise}\n"
    f"Sunset: {sunset}"
)

print(Panel(message, expand=False))

timestamp = response.get("dt")
with open(f"{timestamp}.json", "w+") as file:
    json.dump(response, file, indent=4)


def get_formatted_datetime(timestamp, formatting):
    return datetime.fromtimestamp(timestamp).strftime(formatting)


if __name__ == "__main__":
    main()
