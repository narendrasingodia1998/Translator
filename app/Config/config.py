import os

from dotenv import load_dotenv

# Load environment variables from .env file
env_file = load_dotenv()

lacto_api_key = os.getenv("LACTO_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
rapid_api_key = os.getenv("RAPID_API_KEY")