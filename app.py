import os
from dotenv import load_dotenv  # ✅ Add this
load_dotenv()  # ✅ Load environment variables before app creation

from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
