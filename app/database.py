import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


MONGO_URL = os.getenv("MONGO_URL")



client = MongoClient(MONGO_URL)


db = client["esclavos"]

users_collection = db["users"]


try:
    client.admin.command("ping")
    print("MongoDB Atlas conectado correctamente")

except Exception as e:
    print("Error MongoDB:", e)