from datetime import datetime

def get_current_time():
  return datetime.now()

# TOOLS = [{},{},{}]

TOOLS = [
  {
    "type": "function",
    "name": "get_current_time",
    "description": "Returns the current date and time",
    "parameters": {
      "type": "object",
      "properties": {},
    }
  }
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
  "get_current_time" : get_current_time
}