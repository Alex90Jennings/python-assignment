import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

uri = os.getenv('MONGO_URI')
client = MongoClient(uri)
db = client["python-assignment"]
collection = db["users"]

diet_preferences = [
    "Vegan", "Vegetarian", "Halal", "Kosher", "Paleo", 
    "Gluten-Free", "Dairy-Free", "Low-Carb", "Keto"
]

def get_employees():
    employees = list(collection.find())
    for employee in employees:
        employee['_id'] = str(employee['_id'])
    return employees

def display_employees():
    employees = get_employees()
    print("\nCompany Employee List")
    print("=" * 150)
    print(f"{'Index':<8}{'First Name':<15}{'Last Name':<15}{'Email':<40}{'Full Time':<10}{'Active':<10}{'Salary (£)':<12}{'Annual Leave':<15}{'Diet Preferences'}")
    print("-" * 150)
    
    for index, emp in enumerate(employees, start=1):
        print(f"{index:<8}{emp.get('firstName', 'N/A'):<15}{emp.get('lastName', 'N/A'):<15}{emp.get('email', 'N/A'):<40}{str(emp.get('isFullTime', 'N/A')):<10}{str(emp.get('isActive', 'N/A')):<10}{str(emp.get('salary', 'N/A')):<12}{str(emp.get('annualLeaveDays', 'N/A')):<15}{emp.get('dietPreferences', 'N/A')}")

def main():
    while True:
        print("\nMain Menu")
        print("1. View Employees")
        print("2. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            display_employees()
        elif choice == "2":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
