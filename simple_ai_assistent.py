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

                print(f"\ntools.py tool: {step.name}")

                print (step)

                if step.name == "get_current_time":
                    result = FUNCTION_NAME_TO_FUNCTION_MAP[step.name]

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

                if step.name == "get_weather_info":
                    result = FUNCTION_NAME_TO_FUNCTION_MAP[step.name]
                    result = result(step.arguments['location'])

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
