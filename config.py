import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

security_key = os.getenv("secret_key")

credential = os.getenv("firebase_cred")



    