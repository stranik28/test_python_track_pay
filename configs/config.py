import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")

db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?async_fallback=True"

secret = os.environ.get("secret_key")
encrypt_algorithm = os.environ.get('encrypt_algorithm')

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_PASS = os.environ.get("SMTP_PASS")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
