from datetime import datetime
import json


def get_current_time():
  return datetime.now().astimezone().isoformat()

def get_weather_info(city):
  return "Rain"

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