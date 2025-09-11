import os
from pathlib import Path
from main import get_bot_activity, set_bot_activity

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# BOT_ACTIVITY_PATH = os.path.join(BASE_DIR, "config", "bot_activity.json")

BASE_DIR = Path(__file__).resolve().parent
BOT_ACTIVITY_PATH = BASE_DIR / "config" / "bot_activity.json"

s = get_bot_activity(path=str(BOT_ACTIVITY_PATH))

print(s)
