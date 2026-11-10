# # ollama pull phi3:mini

# from openai import OpenAI
# from dotenv import load_dotenv
# from google import genai

# import os

# load_dotenv()

# # client = OpenAI()
# client = genai.Client(api_key=os.getenv("API_KEY"))

# # client = OpenAI(
# #   base_url = os.getenv("BASE_URL"),
# #   api_key=os.getenv("API_KEY")
# # )

# messages = []

# while True:

#   user_input = input("\nUser: ")

#   if user_input.lower() in ["quit", "exit", "bye"]:
#     break

#   messages.append({"role": "user", "parts":  [{ "text": user_input } ]})

#   # completion = client.chat.completions.create(
#   #   model=os.getenv("MODEL"),
#   #   messages = messages
#   # )

#   interaction = client.interactions.create(
#       model=os.getenv("MODEL"),
#       contents=messages
#   )
#   # print(interaction.output_text)

#   # role - Who is speaking
#   # content - What they said

#   content = interaction.output_text

#   print(content)

#   messages.append({"role": "model", "parts": [{ "text": content }] })

# sudo systemctl stop ollama

# sudo lsof -i :11434 -> Find the process using port 11434:

# kill 1234



from dotenv import load_dotenv
from google import genai
from datetime import datetime
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))

model = os.getenv("MODEL")

previous_interaction_id = None

def get_current_time():
  return datetime.now().astimezone().isoformat()

# get_current_time_function = TOOLS[0]

# system_instruction="""
# You are a helpful AI assistant.
# Answer clearly and accurately.
# Maintain context throughout the conversation.
# Use the get_current_time tool whenever the user
# asks about the current date or time.
# """,


while True:

    user_input = input("\nUser: ")

    if user_input.lower() in ["quit", "exit", "bye"]:
        break

    interaction = client.interactions.create(
        model=model,
        input=user_input,
        previous_interaction_id=previous_interaction_id,
        # system_instruction=system_instruction,
        tools=TOOLS
    )

    # 4. Handle tool calls
    while True:

        function_results = []

        for step in interaction.steps or []:

            if step.type == "function_call":

                print(f"\nCalling tool: {step.name}")

                if step.name == "get_current_time":
                    result = get_current_time()

                    function_results.append({
                        "type": "function_result",
                        "name": step.name,
                        "call_id": step.id,
                        "result": [
                            {
                                "type": "text",
                                "text": json.dumps(result)
                            }
                        ]
                    })

        # No more tool calls
        if not function_results:
            break

        # 5. Send tool results back to Gemini
        interaction = client.interactions.create(
            model=model,
            input=function_results,
            previous_interaction_id=interaction.id,
            # system_instruction=system_instruction,
            tools=TOOLS
        )

    content = interaction.output_text

    print("\nGemini:", content)

    # Save conversation reference
    previous_interaction_id = interaction.id
