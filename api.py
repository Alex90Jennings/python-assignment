import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()
uri = os.getenv('MONGO_URI')
client = MongoClient(uri)
db = client["python-assignment"]
collection = db["users"]

def get_employees():
    employees = list(collection.find())
    for employee in employees:
        employee['_id'] = str(employee['_id'])
    return employees

def get_employee(field, value):
    return collection.find_one({field: value})

def insert_employee(employee):
    return collection.insert_one(employee)

def find_and_update_employee(_id, update_field, value):
    return collection.update_one(
        {"_id": ObjectId(_id)},
        {"$set": {update_field: value}}
    )

def del_employee(_id):
    collection.delete_one({"_id": ObjectId(_id)})