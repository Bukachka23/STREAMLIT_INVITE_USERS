import os


class ConfigDatabase:
    HOST = os.getenv("DB_HOST")
    DB = os.getenv("DB_NAME")
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")
