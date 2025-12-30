
import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

print(f"Project root: {PROJECT_ROOT}")

try:
    from scripts import config
    print("Config module imported")
    try:
        cfg = config.get_config()
        print("Config loaded successfully")
        print(cfg)
    except Exception as e:
        print(f"Error getting config: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"Error importing config: {e}")
    import traceback
    traceback.print_exc()
