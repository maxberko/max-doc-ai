import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
print(f"Project root: {PROJECT_ROOT}")

from scripts.screenshot.gemini_client import GeminiComputerUseClient
from scripts.screenshot.computer_use_tools import ComputerUseTool
import scripts.config as config

async def test_gemini_capture():
    print("🧪 Testing Gemini Computer Use Adapter...")
    
    # Load config
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in env")
        return

    print(f"🔑 Key found: {api_key[:10]}...")

    # Initialize client
    client = GeminiComputerUseClient(api_key=api_key)
    
    # Initialize tool executor (no-op for test if no display, but we want to test flow)
    # We use a dummy width/height
    tools = ComputerUseTool(display_width=1024, display_height=768)
    client.set_tool_executor(tools)

    print("🤖 Client initialized. Sending task...")

    # Define a simple task
    task = "Navigate to youtube.com/ and take a screenshot."

    try:
        # Run the agent loop
        result = await client.execute_task(
            task_prompt=task,
            max_iterations=5, # Limit iterations
            verbose=True
        )

        if result['success']:
            print("✅ Task completed successfully!")
            print(f"📸 Screenshots captured: {len(result['screenshots'])}")
        else:
            print("❌ Task failed or timed out.")

    except Exception as e:
        print(f"❌ Exception during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gemini_capture())
