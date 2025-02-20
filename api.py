import random
from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker
import os

app = Flask(__name__)
fake = Faker('en_GB')

uri = os.getenv('MONGO_URI')
print(f"MongoDB URI: {uri}")

client = MongoClient(uri, server_api=ServerApi('1'))
db = client["python-assignment"]
collection = db["users"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

def get_employees():
    employees = list(collection.find())
    for employee in employees:
        employee['_id'] = str(employee['_id'])
    return employees
    