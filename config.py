from dotenv import load_dotenv
import os

if os.getenv("APP_ENV") == "PROD":
    load_dotenv(".env.prod")
else: # APP_ENV == "DEV"
    load_dotenv(".env.dev")

SERVER = os.getenv("SERVER")
PORT = int(os.getenv("PORT"))
DEBUG = bool(os.getenv("DEBUG"))