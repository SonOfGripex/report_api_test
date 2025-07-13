import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    api_layer_key = os.getenv("APILAYER_KEY")
    openai_key = os.getenv("OPENAI_KEY")
    secret_token = os.getenv("SECRET_TOKEN")


settings = Settings()