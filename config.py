import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CATEGORY_ID = int(os.getenv("CATEGORY_ID", 0))
CANAL_LOGS_ID = int(os.getenv("CANAL_LOGS_ID", 0))
NOME_CARGO_SUPORTE = os.getenv("NOME_CARGO_SUPORTE", "Suporte")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "bot_atendimento")
}