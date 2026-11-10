from datetime import datetime
import requests

def get_current_time():
  return datetime.now().astimezone().isoformat()

def get_weather_info(city):
    url = f"https://wttr.in{city}?format=j1"

    try:
        response = requests.get(url)
        response.raise_for_status() # Raises an error for bad responses
        data = response.json()

        # Parse current condition details
        current = data['current_condition'][0]
        temp_c = current['temp_C']
        weather_desc = current['weatherDesc'][0]['value']
        humidity = current['humidity']

        print(f"Weather in {city}:")
        print(f"Temperature: {temp_c}°C")
        print(f"Condition: {weather_desc}")
        print(f"Humidity: {humidity}%")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")


TOOLS = [
  {
    "type": "function",
    "name": "get_current_time",
    "description": "Returns the current date and time",
    "parameters": {
      "type": "object",
      "properties": {},
    }
  },
  {
    "type": "function",
    "name": "get_weather_info",
    "description": "Returns the current weather of the given city",
    "parameters": {
      "type": "string",
      "properties": {
          "city": {
              "type": "string",
              "description": "Name of the city"
          }
        },
        "required": ["city"]
    }
  }
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
  "get_current_time" : get_current_time,
  "get_weather_info" : get_weather_info
}