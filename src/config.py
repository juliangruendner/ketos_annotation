import os

POSTGRES_USER = str(os.getenv('POSTGRES_USER', ''))
POSTGRES_PASSWORD = str(os.getenv('POSTGRES_PASSWORD', ''))
POSTGRES_DB = str(os.getenv('POSTGRES_DB', ''))
