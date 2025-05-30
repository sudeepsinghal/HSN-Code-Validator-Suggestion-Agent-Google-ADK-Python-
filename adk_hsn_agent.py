from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Updated import paths based on the new file names
from hsn_data_loader import HSNDataLoader
from hsn_code_validator import HSNCodeValidator
from hsn_code_suggestor import HSNCodeSuggestor
from hsn_error_handler import HSNErrorHandler

import os
import asyncio
import json

with open("C:\python\projects\HSN_using_adk\env.json" , "r") as f:
    env = json.load(f)

# --- Agent Setup ---
# IMPORTANT: Your provided API key is placed here.
os.environ["GOOGLE_API_KEY"] = env["store"]

class HSNCodeAgent:
    def __init__(self, excel_file_path="HSN_SAC.xlsx"):
        # Updated class names for instantiation
        self.loader = HSNDataLoader(excel_file_path)
        self.df = self.loader.get_dataframe()
        self.validator = HSNCodeValidator(self.df)
        self.suggestor = HSNCodeSuggestor(self.df)

    def validate_hsn_code(self, code: str) -> str:

        is_valid, result = self.validator.validate_code(code)
        if is_valid:
            parents = self.validator.validate_hierarchy(code)
            parent_info = f"Parent Codes: {parents}" if parents else "No parent codes found."
            return f"Valid HSN Code: {code} — {result}. {parent_info}"
        else:
            return f"Invalid HSN Code: {result}"

    def suggest_hsn_codes(self, description: str) -> str:

        suggestions = self.suggestor.suggest(description)
        if isinstance(suggestions, str):
            return f"Suggestion: {suggestions}"
        else:
            formatted_suggestions = ["Suggestions:"]
            for _, row in suggestions.iterrows():
                formatted_suggestions.append(f"{row['HSNCode']} — {row['Description']}")
            return "\n".join(formatted_suggestions)

def create_hsn_agent():
    hsn_logic = HSNCodeAgent()

    validate_tool = FunctionTool(func=hsn_logic.validate_hsn_code)

    suggest_tool = FunctionTool(func=hsn_logic.suggest_hsn_codes)

    agent = LlmAgent(
        name="hsn_code_validator_and_suggestor",
        description="An agent that can validate HSN codes, check their hierarchy, and suggest HSN codes based on product/service descriptions.",
        instruction="You are an expert assistant for Harmonized System Nomenclature (HSN) codes. Your primary function is to validate HSN codes or suggest them based on descriptions. When a user provides a numeric input, use the validate_hsn_code tool. When a user provides a textual description, use the suggest_hsn_codes tool. Always be helpful and informative.",
        model="gemini-1.5-flash-latest",
        tools=[validate_tool, suggest_tool]
    )
    return agent

async def run_hsn_agent():
    agent = create_hsn_agent()
    APP_NAME = "hsn_validation_app"
    USER_ID = "user_123"
    SESSION_ID = "session_456"

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    print("HSN Code Validator and Suggestion Agent")
    print("Type 'exit' to quit. Provide an HSN code (e.g., '01011010') or a product/service description (e.g., 'live horses').")

    while True:
        user_input = input("Enter HSN code or description: ").strip()
        if user_input.lower() == 'exit':
            print("Exiting.")
            break

        content = types.Content(role="user", parts=[types.Part(text=user_input)])
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
            if event.is_final_response():
                print(f"Agent Response: {event.content.parts[0].text}")

if __name__ == "__main__":
    asyncio.run(run_hsn_agent())