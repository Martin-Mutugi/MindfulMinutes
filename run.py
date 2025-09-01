from dotenv import load_dotenv
load_dotenv()

from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    # Explicitly set the Flask app name for CLI and debugger
    app.run(debug=True)
