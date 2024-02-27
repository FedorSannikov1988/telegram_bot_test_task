"""
Loading all necessary parameters, addresses,
token, keys from environment variables.
"""
from dotenv import load_dotenv
import os

load_dotenv()

ID_MANAGER = int(os.getenv('ID_MANAGER'))
TOKEN_BOT = os.getenv('TOKEN_FOR_BOT')
