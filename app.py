import os
import re
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

def is_valid_name(name):
    if not name:
        return False, "Name cannot be empty."
    if not name.isalpha():
        return False, "Name must contain only letters."
    if not 2 <= len(name) <= 15:
        return False, "Name must be between 2 and 15 characters long."
    return True, ""

def is_valid_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email format."
    if collection.find_one({"email": email}):
        return False, "Email must be unique."
    return True, ""

def is_valid_salary(value, isFullTime):
    try:
        is_valid_positive_number(value)
        if isFullTime and value <= 20000:
            return False, "Full time employees must earn more than 20000."
        if not isFullTime and value < 10000:
            return False, "Full time employees must earn more than 10000."
        return True, ""
    except ValueError:
        return False, "Value must be a number."
    
def is_valid_leave_days(value):
    try:
        is_valid_positive_number(value)
        if value <= 0:
            return False, "Number must be positive."
        if value < 10:
            return False, "Annual leave days should be above 10."
        if value > 30:
            return False, "Annual leave days should be below 30."
        return True, ""
    except ValueError:
        return False, "Value must be a number."

def is_valid_positive_number(value):
    try:
        num = float(value)
        if num <= 0:
            return False, "Number must be positive."
        return True, ""
    except ValueError:
        return False, "Value must be a number."

def is_valid_boolean(value):
    if isinstance(value, bool):
        return True, ""
    return False, "Must be either 'true', 'false'"

def is_valid_diet_preference(value):
    if value not in diet_preferences:
        return False, f"Diet preference must be one of: {', '.join(diet_preferences)}."
    return True, ""

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
    print("\nSelected Employee for Update")
    print_separator("=")
    print(get_table_headers())
    print_separator("-")
    print(print_employee_details(employee, index))
    print_separator("-")

def update_employee():
    employees = get_employees()
    if not employees:
        print("\nNo employees found.")
        return
    display_employees()
    try:
        index = int(input("\nEnter the index of the employee to update: ")) - 1
        if index < 0 or index >= len(employees):
            print("Invalid index. Please try again.")
            return
        employee = employees[index]
        display_single_employee(employee, index + 1)

        print("\nWhat would you like to update?")
        print("1. First Name")
        print("2. Last Name")
        print("3. Email")
        print("4. Full Time")
        print("5. Active")
        print("6. Salary")
        print("7. Annual Leave")
        print("8. Diet Preferences")
        choice = input("Enter the number of the attribute to update: ")

        update_field = ""
        if choice == "1":
            update_field = "firstName"
        elif choice == "2":
            update_field = "lastName"
        elif choice == "3":
            update_field = "email"
        elif choice == "4":
            update_field = "isFullTime"
        elif choice == "5":
            update_field = "isActive"
        elif choice == "6":
            update_field = "salary"
        elif choice == "7":
            update_field = "annualLeaveDays"
        elif choice == "8":
            update_field = "dietPreferences"
        else:
            print("Invalid choice.")
            return

        if update_field == "dietPreferences":
            print("\nAvailable Diet Preferences:")
            for i, preference in enumerate(diet_preferences, start=1):
                print(f"{i}. {preference}")
            user_input = input("\nEnter the numbers of your diet preferences, separated by commas (up to 2): ").strip()

            if user_input == "":
                new_value = []
                print("No diet preferences selected.")
            else:
                try:
                    selected_numbers = [int(num.strip()) for num in user_input.split(',')]
                    if len(selected_numbers) < 0 or len(selected_numbers) > 2:
                        print("You must select between 0 and 2 preferences.")
                        return
                    selected_preferences = []
                    for num in selected_numbers:
                        if 1 <= num <= len(diet_preferences):
                            selected_preferences.append(diet_preferences[num - 1])
                        else:
                            print(f"Invalid number {num}. Please select a valid number between 1 and {len(diet_preferences)}.")
                            return
                    new_value = selected_preferences
                    print(new_value)
                except ValueError:
                    print("Invalid input. Please enter valid numbers.")
                    return

        elif update_field == "isFullTime" or update_field == "isActive":
            new_value = input(f"Enter the new value for {update_field} (true/false): ").strip().lower()
            if new_value not in ["true", "false"]:
                print("Invalid input. Please enter 'true' or 'false'.")
                return
            new_value = new_value in ["true"]

        else:
            new_value = input(f"Enter the new value for {update_field}: ").strip()

        if update_field == "firstName" or update_field == "lastName":
            is_valid, message = is_valid_name(new_value)
            if not is_valid:
                print(message)
                return

        elif update_field == "email":
            is_valid, message = is_valid_email(new_value)
            if not is_valid:
                print(message)
                return

        elif update_field == "annualLeaveDays":
            is_valid, message = is_valid_leave_days(new_value)
            if not is_valid:
                print(message)
                return
            
        elif update_field == "salary":
            is_valid, message = is_valid_salary(new_value, employee.get('isFullTime'))
            if not is_valid:
                print(message)
                return

        elif update_field == "isFullTime" or update_field == "isActive":
            is_valid, message = is_valid_boolean(new_value)
            if not is_valid:
                print(message)
                return

        elif update_field == "dietPreferences":
            for preference in new_value:
                is_valid, message = is_valid_diet_preference(preference)
                if not is_valid:
                    print(message)
                    return

        collection.update_one(
            {"_id": ObjectId(employee["_id"])},
            {"$set": {update_field: new_value}}
        )
        print(f"\nEmployee {update_field} updated successfully!")

    except ValueError:
        print("Invalid input. Please enter a valid number.")

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
        print("3. Update Employee")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            display_employees()
        elif choice == "2":
            delete_employee()
        elif choice == "3":
            update_employee()
        elif choice == "4":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
