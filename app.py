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

DIET_PREFERENCES = ["Vegan", "Vegetarian", "Halal", "Kosher", "Paleo", "Gluten-Free", "Dairy-Free", "Low-Carb", "Keto"]

def print_separator(symbol, length=158):
    print(symbol * length)

def print_employee_details(employee, index):
    return f"{index:<8}{employee.get('firstName', 'N/A'):<15}{employee.get('lastName', 'N/A'):<15}{employee.get('email', 'N/A'):<40}{str(employee.get('isFullTime', 'N/A')):<14}{str(employee.get('isActive', 'N/A')):<10}{str(employee.get('salary', 'N/A')):<14}{str(employee.get('annualLeaveDays', 'N/A')):<15}{employee.get('dietPreferences', 'N/A')}"

def get_employees():
    employees = list(collection.find())
    for employee in employees:
        employee['_id'] = str(employee['_id'])
    return employees

def get_table_headers():
    return f"{'Index':<8}{'First Name':<15}{'Last Name':<15}{'Email':<40}{'Full Time':<14}{'Active':<10}{'Salary (£)':<14}{'Annual Leave':<15}{'Diet Preferences'}"

def is_valid_boolean(value):
    if isinstance(value, bool):
        return True, ""
    return False, "Must be either 'true', 'false'"

def is_valid_positive_number(value):
    try:
        num = float(value)
        if num <= 0:
            return False, "Number must be positive."
        return True, ""
    except ValueError:
        return False, "Value must be a number."

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

def is_valid_salary(value, is_full_time):
    is_valid, message = is_valid_positive_number(value)
    if not is_valid:
        return False, message
    if is_full_time and float(value) <= 20000:
        return False, "Full time employees must earn more than 20000."
    if not is_full_time and float(value) < 10000:
        return False, "Part time employees must earn more than 10000."
    return True, ""

def is_valid_leave_days(value):
    is_valid, message = is_valid_positive_number(value)
    if not is_valid:
        return False, message
    if float(value) < 10:
        return False, "Annual leave days should be above 10."
    if float(value) > 30:
        return False, "Annual leave days should be below 30."
    return True, ""

def is_valid_diet_preference(value):
    if value not in DIET_PREFERENCES:
        return False, f"Diet preference must be one of: {', '.join(DIET_PREFERENCES)}."
    return True, ""

def create_employee():
    print("\nCreate New Employee")
    
    first_name = input("Enter First Name: ").strip()
    last_name = input("Enter Last Name: ").strip()
    email = input("Enter Email: ").strip()

    if not (valid := is_valid_name(first_name))[0]:
        print(valid[1])
        return
    if not (valid := is_valid_name(last_name))[0]:
        print(valid[1])
        return
    if not (valid := is_valid_email(email))[0]:
        print(valid[1])
        return

    is_full_time = input("Is the employee full-time? (true/false): ").strip().lower()
    if is_full_time not in ["true", "false"]:
        print("Invalid input. Please enter 'true' or 'false'.")
        return
    is_full_time = is_full_time == "true"

    salary = input(f"Enter Salary for {first_name} {last_name}: ").strip()
    if not (valid := is_valid_salary(salary, is_full_time))[0]:
        print(valid[1])
        return

    annual_leave = input("Enter Annual Leave Days: ").strip()
    if not (valid := is_valid_leave_days(annual_leave))[0]:
        print(valid[1])
        return

    diet_preferences = select_diet_preferences()

    employee = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "isFullTime": is_full_time,
        "isActive": True,
        "salary": round(float(salary)),
        "annualLeaveDays": round(float(annual_leave)),
        "dietPreferences": diet_preferences
    }

    collection.insert_one(employee)
    print(f"\nEmployee {first_name} {last_name} created successfully!")

def select_diet_preferences():
    print("\nAvailable Diet Preferences:")
    for i, preference in enumerate(DIET_PREFERENCES, start=1):
        print(f"{i}. {preference}")
    
    user_input = input("Enter the numbers of diet preferences (separate by commas, up to 2): ").strip()
    if user_input:
        try:
            selected_numbers = [int(num.strip()) for num in user_input.split(',')]
            if len(selected_numbers) < 0 or len(selected_numbers) > 2:
                print("You must select between 0 and 2 preferences.")
                return []
            selected_preferences = [DIET_PREFERENCES[num - 1] for num in selected_numbers if 1 <= num <= len(DIET_PREFERENCES)]
            return selected_preferences
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            return []
    return []

def update_options():
    print("\nWhat would you like to update?")
    print("1. First Name")
    print("2. Last Name")
    print("3. Email")
    print("4. Full Time")
    print("5. Active")
    print("6. Salary")
    print("7. Annual Leave")
    print("8. Diet Preferences")

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
        update_options()
        choice = input("Enter the number of the attribute to update: ")

        update_field = map_update_choice_to_field(choice)
        if not update_field:
            print("Invalid choice.")
            return

        new_value = get_new_value(update_field)
        if new_value is None:
            return

        collection.update_one(
            {"_id": ObjectId(employee["_id"])},
            {"$set": {update_field: new_value}}
        )
        print(f"Employee {employee['email']} updated successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_new_value(update_field):
    if update_field == "dietPreferences":
        return select_diet_preferences()
    elif update_field == "isFullTime" or update_field == "isActive":
        new_value = input(f"Enter the new value for {update_field} (true/false): ").strip().lower()
        if new_value not in ["true", "false"]:
            print("Invalid input. Please enter 'true' or 'false'.")
            return None
        return new_value == "true"
    else:
        new_value = input(f"Enter the new value for {update_field}: ").strip()
        if update_field == "salary" or update_field == "annualLeaveDays":
            return round(float(new_value))
        else:
            return new_value

def map_update_choice_to_field(choice):
    field_map = {
        "1": "firstName",
        "2": "lastName",
        "3": "email",
        "4": "isFullTime",
        "5": "isActive",
        "6": "salary",
        "7": "annualLeaveDays",
        "8": "dietPreferences"
    }
    return field_map.get(choice)

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
        collection.delete_one({"_id": ObjectId(employee["_id"])})
        print(f"Employee {employee['email']} deleted successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def display_single_employee(employee, index):
    print("\nEmployee Details:")
    print(f"Index: {index}")
    print_employee_details(employee, index)

def display_employees():
    print(get_table_headers())
    employees = get_employees()
    for idx, employee in enumerate(employees, start=1):
        print(print_employee_details(employee, idx))

def main_options():
    print_separator("-")
    print("Employee Management System")
    print_separator("-")
    print("1. Create Employee")
    print("2. View All Employees")
    print("3. Update Employee")
    print("4. Delete Employee")
    print("5. Exit")

def main():
    while True:
        try:
            main_options()
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                create_employee()
            elif choice == "2":
                display_employees()
            elif choice == "3":
                update_employee()
            elif choice == "4":
                delete_employee()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting the program...")  # Custom exit message
            break

if __name__ == "__main__":
    main()
