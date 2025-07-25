import os
import subprocess
import requests

REPO_URL = "https://github.com/Tadelachewu/SecurityBotSystem.git"
REPO_DIR = "SecurityBotSystem"

# Clone the repo if not already cloned
if not os.path.exists(REPO_DIR):
    print("Cloning repo...")
    subprocess.run(["git", "clone", REPO_URL])
else:
    print("Repo already exists.")

# Run the bot or script inside
script_path = os.path.join(REPO_DIR, "securityBot.py")
if os.path.exists(script_path):
    print("Running the bot...")
    subprocess.run(["python", script_path])
else:
    print("No 'securityBot.py' found in the repo.")
