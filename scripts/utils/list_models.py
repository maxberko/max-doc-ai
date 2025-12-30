
import os
import sys
from pathlib import Path
import google.generativeai as genai

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load config to get key (or get from env directly since we set it)
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ No API key found")
    sys.exit(1)

genai.configure(api_key=api_key)

print("🔍 Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"❌ Error listing models: {e}")
