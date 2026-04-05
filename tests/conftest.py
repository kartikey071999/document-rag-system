import os
from pathlib import Path

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

base_dir = Path(__file__).resolve().parent.parent
env_file = base_dir / ".env"
if not env_file.exists():
    with open(env_file, "w") as f:
        f.write("SECRET_KEY=test-secret-key-for-testing-only\n")
        f.write("DEBUG=True\n")
        f.write("GEMINI_API_KEY=test-api-key\n")

django.setup()
