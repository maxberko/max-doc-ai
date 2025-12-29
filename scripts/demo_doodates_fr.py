http///localhost/8080/DooDates/date-polls/dashboard
import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Ensure config environment variables are set if not present
if not os.getenv("GOOGLE_API_KEY"):
    import scripts.config as cfg
    # Attempt to load from .env or config if not in env
    # (Assuming config.py logic works, but for this standalone script we might need to be explicit if .env isn't auto-loaded)
    from dotenv import load_dotenv
    load_dotenv()

from scripts.screenshot.gemini_client import GeminiComputerUseClient
from scripts.screenshot.computer_use_tools import ComputerUseTool

async def generate_doodates_doc():
    print("🚀 Starting DooDates Documentation Test (Gemini Powered)...")
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found.")
        return

    # Initialize Client & Tools
    # We use a standard viewport
    client = GeminiComputerUseClient(
        api_key=api_key,
        model="gemini-2.5-flash", 
        display_width=1280,
        display_height=800
    )
    
    tools = ComputerUseTool(display_width=1280, display_height=800)
    client.set_tool_executor(tools)

    # The Target URL (from user state)
    target_url = "http://localhost:8080/DooDates/date-polls/dashboard"
    
    prompt = f"""
    OBJECTIF : Créer un extrait de documentation interne pour le 'Dashboard DooDates'.

    1. Naviguer vers {target_url}
    2. Attendre que la page soit complètement chargée (vérifier la présence du tableau ou des graphiques).
    3. Prendre une capture d'écran du dashboard.
    4. Analyser la capture d'écran et rédiger un paragraphe de documentation technique interne (en FRANÇAIS) décrivant les fonctionnalités visibles.
    
    Format souhaité :
    - Titre : Vue d'ensemble du Tableau de Bord
    - Description : Ce que l'outil permet de piloter.
    - Points clés : Liste à puces des éléments visuels identifiés.
    
    Affichez le texte final de la documentation dans votre réponse.
    """

    print(f"🎯 Target: {target_url}")
    print("⏳ Executing Agent Loop...")

    try:
        result = await client.execute_task(
            task_prompt=prompt,
            max_iterations=10,
            verbose=True
        )

        if result['success']:
            print("\n✅ DOC GENERATION SUCCESSFUL!")
            
            # Find the last message from the model to get the doc text
            messages = result.get('messages', [])
            if messages:
                last_msg = messages[-1]
                print("\n📄 Generated Documentation:\n")
                print("="*40)
                print(last_msg.get('content', 'No content'))
                print("="*40)
            
            print(f"\n📸 Screenshots captured: {len(result.get('screenshots', []))}")
        else:
            print("❌ Task failed or timed out.")

    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(generate_doodates_doc())
