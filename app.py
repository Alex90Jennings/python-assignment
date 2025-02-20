import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
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

def get_table_headers():
    return f"{'Index':<8}{'First Name':<15}{'Last Name':<15}{'Email':<40}{'Full Time':<14}{'Active':<10}{'Salary (£)':<14}{'Annual Leave':<15}{'Diet Preferences'}"

def print_separator(symbol, length=158):
    print(symbol * length)

def print_employee_details(employee, index):
    return f"{index:<8}{employee.get('firstName', 'N/A'):<15}{employee.get('lastName', 'N/A'):<15}{employee.get('email', 'N/A'):<40}{str(employee.get('isFullTime', 'N/A')):<14}{str(employee.get('isActive', 'N/A')):<10}{str(employee.get('salary', 'N/A')):<14}{str(employee.get('annualLeaveDays', 'N/A')):<15}{employee.get('dietPreferences', 'N/A')}"

def display_employees():
    employees = get_employees()
    if not employees:
        print("\nNo employees found.")
        return
    print("\nCompany Employee List")
    print_separator("=")
    print(get_table_headers())
    print_separator("-")
    for index, emp in enumerate(employees, start=1):
        print(print_employee_details(emp, index))

def display_single_employee(employee, index):
    print("\nSelected Employee for Deletion")
    print_separator("=")
    print(get_table_headers())
    print_separator("-")
    print(print_employee_details(employee, index))
    print_separator("-")

def delete_employee():
    employees = get_employees()
    if not employees:
        print("\nNo employees found.")
        return
    display_employees()
    try:
        index = int(input("\nEnter the index of the employee to delete: ")) - 1
        if index < 0 or index >= len(employees):
            print("Invalid index. Please try again.")
            return
        employee = employees[index]
        display_single_employee(employee, index + 1)
        confirm = input("Are you sure you want to delete this employee? (yes/no): ").strip().lower()
        if confirm == "yes":
            collection.delete_one({"_id": ObjectId(employee["_id"])})
            print("\nEmployee deleted successfully!")
        else:
            print("\nDeletion cancelled.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def main():
    while True:
        print("\nMain Menu")
        print("1. View Employees")
        print("2. Delete Employee")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            display_employees()
        elif choice == "2":
            delete_employee()
        elif choice == "3":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
