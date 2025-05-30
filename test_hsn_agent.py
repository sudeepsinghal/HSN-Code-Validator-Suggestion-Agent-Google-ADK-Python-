import asyncio
import pandas as pd
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import the create_hsn_agent function from your main agent file
from adk_hsn_agent import create_hsn_agent

# --- Configuration ---
EXCEL_FILE_PATH = "HSN_SAC.xlsx"
APP_NAME = "hsn_validation_app"
USER_ID = "test_user"
SESSION_ID = "test_session_1"

async def run_automated_tests():
    print("Setting up agent for automated testing...")
    agent = create_hsn_agent()
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
        # Fix for newline character in column name
        df.columns = df.columns.str.strip()
        print(f"Loaded {len(df)} entries from {EXCEL_FILE_PATH}")
        print(f"Actual columns found in Excel (after strip): {df.columns.tolist()}")
    except FileNotFoundError:
        print(f"Error: Excel file not found at {EXCEL_FILE_PATH}")
        return
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    print("\n--- Starting Automated HSN Code Validation Tests ---")
    for index, row in df.iterrows():
        hsn_code = str(row['HSNCode']) # Ensure HSNCode is treated as string
        description = str(row['Description']) # Ensure description is string

        # Test 1: Validate HSN Code
        print(f"\nTesting Validation for HSN Code: {hsn_code}")
        validate_query = f"Validate HSN code {hsn_code}"
        content = types.Content(role="user", parts=[types.Part(text=validate_query)])
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
            if event.is_final_response():
                print(f"Agent Response (Validation): {event.content.parts[0].text}")

        # Test 2: Suggest for Description
        print(f"Testing Suggestion for Description: '{description}'")
        suggest_query = f"Suggest HSN codes for '{description}'"
        content = types.Content(role="user", parts=[types.Part(text=suggest_query)])
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
            if event.is_final_response():
                print(f"Agent Response (Suggestion): {event.content.parts[0].text}")

        # FIX: Add a delay to avoid hitting API rate limits
        # A 4-second delay per iteration (2 API calls) ensures you stay within ~15 requests/minute (30s per 2 calls)
        await asyncio.sleep(8) # Adjust this value if you still hit rate limits or want to speed up

    print("\n--- Automated Testing Complete ---")

if __name__ == "__main__":
    asyncio.run(run_automated_tests())