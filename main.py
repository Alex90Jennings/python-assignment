from api import del_employee, find_and_update_employee, get_employees, insert_employee
from console import display_employees, display_single_employee, main_options, update_options
from utils import ReturnToMenuException, get_input, get_new_value, map_update_choice_to_field, select_diet_preferences
from validators import is_valid_email, is_valid_leave_days, is_valid_name, is_valid_salary


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
                print("\nExiting the program...")
                break
            else:
                print("Invalid choice. Please try again.")
        except ReturnToMenuException:
            print("\nReturning to the main menu...\n")
            continue
        except KeyboardInterrupt:
            print("\nExiting the program...")
            break

def create_employee():
    print("\nCreate New Employee\n")
    
    first_name = get_input("Enter First Name: ").strip()
    if not (valid := is_valid_name(first_name))[0]:
        print(valid[1])
        return

    last_name = get_input("Enter Last Name: ").strip()
    if not (valid := is_valid_name(last_name))[0]:
        print(valid[1])
        return

    email = get_input("Enter Email: ").strip()
    if not (valid := is_valid_email(email))[0]:
        print(valid[1])
        return

    is_full_time = get_input("Is the employee full-time? (true/false): ").strip().lower()
    if is_full_time not in ["true", "false"]:
        print("Invalid input. Please enter 'true' or 'false'.")
        return
    is_full_time = is_full_time == "true"

    salary = get_input(f"Enter Salary for {first_name} {last_name}: ").strip()
    if not (valid := is_valid_salary(salary, is_full_time))[0]:
        print(valid[1])
        return

    annual_leave = get_input("Enter Annual Leave Days: ").strip()
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

    insert_employee(employee)
    print(f"\nEmployee with {email} created successfully!")

def fetch_and_display_employees():
    employees = get_employees()
    if not employees:
        print("\nNo employees found.")
        return
    
    display_employees(employees)
    
    index = int(get_input("\nEnter the index of the employee to focus on: ")) - 1
    if index < 0 or index >= len(employees):
        print("Invalid index. Please try again.")
        return

    display_single_employee(employees[index], index + 1)


def update_employee():
    employees = get_employees()
    if not employees:
        print("\nNo employees found.")
        return
    print("\n")
    display_employees(employees)
    print("\n")
    try:
        index = int(get_input("\nEnter the index of the employee to update: ")) - 1
        if index < 0 or index >= len(employees):
            print("Invalid index. Please try again.")
            return
        employee = employees[index]
        display_single_employee(employee, index + 1)
        update_options()
        choice = get_input("Enter the number of the attribute to update: ")

        update_field = map_update_choice_to_field(choice)
        if not update_field:
            print("Invalid choice.")
            return

        new_value = get_new_value(update_field)
        if new_value is None:
            return
        
        find_and_update_employee(employee["_id"], update_field, new_value)
        print(f"Employee {employee['email']} updated successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_employee():
    employees = get_employees()
    if not employees:
        print("\nNo employees found.")
        return
    display_employees(employees)
    try:
        index = int(get_input("\nEnter the index of the employee to delete: \n")) - 1
        if index < 0 or index >= len(employees):
            print("Invalid index. Please try again.")
            return
        employee = employees[index]
        del_employee(employee["_id"])
        print(f"Employee {employee['email']} deleted successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
