from api import del_employee, find_and_update_employee, get_employees, insert_employee
from console import display_employees, display_single_employee, main_options, update_options
from utils import ReturnToMenuException, get_input, get_new_value, map_update_choice_to_field, select_diet_preferences, get_valid_choice, get_valid_index, get_valid_input
from validators import is_valid_email, is_valid_employee, is_valid_leave_days, is_valid_name, is_valid_salary

def main_menu():
    while True:
        try:
            main_options()
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                create_employee()
            elif choice == "2":
                fetch_and_display_employees()
            elif choice == "3":
                update_employee()
            elif choice == "4":
                delete_employee()
            elif choice == "5":
                print("\nExiting the program...\n")
                break
            else:
                print("Invalid choice. Please try again.\n")
        except ReturnToMenuException:
            print("\nReturning to the main menu...\n")
            continue
        except KeyboardInterrupt:
            print("\nExiting the program...\n")
            break

def get_valid_employees():
    fetched_employees = get_employees()
    if not fetched_employees:
        print("\nNo employees found.")
        return
    employees = []
    for employee in fetched_employees:
        valid_employee = is_valid_employee(employee)
        if valid_employee:
            employees.append(valid_employee)
    return employees

def fetch_and_display_employees():
    employees = get_valid_employees()
    display_employees(employees)
    while True:
        user_input = get_input("\nEnter the index of the employee to focus on: ").strip()
        try:
            index = int(user_input) - 1
            if index < 0 or index >= len(employees):
                print("Invalid index. Please try again.\n")
            else:
                display_single_employee(employees[index], index + 1)
        except ValueError:
            print("Invalid input. Please enter a valid index or 'exit' to quit.\n")

def create_employee():
    print("\nCreate New Employee\n")
    first_name = get_valid_input("Enter First Name: ", is_valid_name)
    last_name = get_valid_input("Enter Last Name: ", is_valid_name)
    email = get_valid_input("Enter Email: ", is_valid_email)
    is_full_time = get_valid_choice("Is the employee full-time? (true/false): ", ["true", "false"]) == "true"
    salary = round(float(get_valid_input(f"Enter Salary for {first_name} {last_name}: ", lambda v: is_valid_salary(v))))
    annual_leave = round(float(get_valid_input("Enter Annual Leave Days: ", is_valid_leave_days)))
    diet_preferences = select_diet_preferences()
    employee = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "isFullTime": is_full_time,
        "isActive": True,
        "salary": salary,
        "annualLeaveDays": annual_leave,
        "dietPreferences": diet_preferences
    }
    valid_employee = is_valid_employee(employee)
    if employee:
        insert_employee(valid_employee)
        print(f"\nEmployee with {email} created successfully!")
    else:
        print(f"\nEmployee could not be added")

def update_employee():
    employees = get_valid_employees()
    display_employees(employees)
    index = get_valid_index("\nEnter the index of the employee to update: ", employees)
    employee = employees[index]
    display_single_employee(employee, index + 1)
    update_options()
    while True:
        choice = get_input("Enter the number of the attribute to update: ")
        update_field = map_update_choice_to_field(choice)
        if update_field:
            break
        print("Invalid choice. Please try again.")
    new_value = get_new_value(update_field)
    find_and_update_employee(employee["_id"], update_field, new_value)
    print(f"\nEmployee {employee['email']} updated successfully!")


def delete_employee():
    employees = get_valid_employees()
    display_employees(employees)
    index = get_valid_index("\nEnter the index of the employee to delete: ", employees)
    employee = employees[index]
    del_employee(employee["_id"])
    print(f"\nEmployee {employee['email']} deleted successfully!")
