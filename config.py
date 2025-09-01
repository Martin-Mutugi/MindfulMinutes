import os

class Config:
    # Core Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')

    # Async-compatible database URI
    RAW_DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    SQLALCHEMY_DATABASE_URI = (
        RAW_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        if RAW_DATABASE_URL.startswith("postgresql://")
        else RAW_DATABASE_URL
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # Hugging Face API
    HF_API_TOKEN = os.getenv('HF_API_TOKEN')

    # Paystack API keys
    PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY")
    PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
