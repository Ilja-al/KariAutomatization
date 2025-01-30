import os

class Data:
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
