import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

GEOLOCATION_URL = "https://ipapi.co/json/"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

WMO_DESCRIPTIONS = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    95: "thunderstorm",
}


def calculator(expression):
    try:
        result = eval(expression)

        return {
            "success": True,
            "result": result,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def get_time():
    now = datetime.now().astimezone()

    return {
        "success": True,
        "time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": str(now.tzinfo),
    }


def _location_from_ipapi():
    response = requests.get(GEOLOCATION_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("error"):
        raise ValueError(data.get("reason", "Could not detect location from IP"))

    return {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "city": data.get("city"),
        "region": data.get("region"),
        "country": data.get("country_name"),
    }


def _location_from_ipwhois():
    response = requests.get("https://ipwho.is/", timeout=10)
    response.raise_for_status()
    data = response.json()

    if not data.get("success"):
        raise ValueError(data.get("message", "Could not detect location from IP"))

    return {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "city": data.get("city"),
        "region": data.get("region"),
        "country": data.get("country"),
    }


def _get_location_from_ip():
    errors = []

    for provider in (_location_from_ipapi, _location_from_ipwhois):
        try:
            return provider()
        except (requests.RequestException, ValueError, KeyError) as e:
            errors.append(str(e))

    raise ValueError("; ".join(errors))


def _weather_from_openweather(location, api_key):
    response = requests.get(
        OPENWEATHER_URL,
        params={
            "lat": location["latitude"],
            "lon": location["longitude"],
            "appid": api_key,
            "units": "metric",
        },
        timeout=10,
    )
    response.raise_for_status()
    weather = response.json()

    return {
        "success": True,
        "provider": "openweathermap",
        "location": {
            "city": location["city"],
            "region": location["region"],
            "country": location["country"],
        },
        "description": weather["weather"][0]["description"],
        "temperature_c": weather["main"]["temp"],
        "feels_like_c": weather["main"]["feels_like"],
        "humidity_percent": weather["main"]["humidity"],
    }


def _weather_from_open_meteo(location):
    response = requests.get(
        OPEN_METEO_URL,
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code",
            "timezone": "auto",
        },
        timeout=10,
    )
    response.raise_for_status()
    weather = response.json()
    current = weather["current"]
    weather_code = current["weather_code"]

    return {
        "success": True,
        "provider": "open-meteo",
        "location": {
            "city": location["city"],
            "region": location["region"],
            "country": location["country"],
        },
        "description": WMO_DESCRIPTIONS.get(weather_code, f"weather code {weather_code}"),
        "temperature_c": current["temperature_2m"],
        "feels_like_c": current["apparent_temperature"],
        "humidity_percent": current["relative_humidity_2m"],
    }


def get_weather():
    try:
        location = _get_location_from_ip()
        api_key = os.getenv("OPENWEATHER_API_KEY") or os.getenv("WEATHER_API_KEY")

        if api_key:
            return _weather_from_openweather(location, api_key)

        return _weather_from_open_meteo(location)

    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Weather API request failed: {e}",
        }
    except (KeyError, ValueError) as e:
        return {
            "success": False,
            "error": f"Could not read weather data: {e}",
        }


def run_tool(tool_name, arguments=None):
    arguments = arguments or {}

    if tool_name == "calculator":
        return calculator(arguments["expression"])
    if tool_name == "getTime":
        return get_time()
    if tool_name == "getWeather":
        return get_weather()

    return {
        "success": False,
        "error": f"Unknown tool: {tool_name}",
    }
