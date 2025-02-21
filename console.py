def print_separator(symbol, length=158):
    print(symbol * length)

def print_employee_details(employee, index):
    diet_prefs = ", ".join(employee.get('dietPreferences', []))
    return f"{index:<8}{employee.get('firstName', 'N/A'):<15}{employee.get('lastName', 'N/A'):<15}{employee.get('email', 'N/A'):<40}{str(employee.get('isFullTime', 'N/A')):<14}{str(employee.get('isActive', 'N/A')):<10}{str(employee.get('salary', 'N/A')):<14}{str(employee.get('annualLeaveDays', 'N/A')):<15}{diet_prefs}"

def get_table_headers():
    return f"{'Index':<8}{'First Name':<15}{'Last Name':<15}{'Email':<40}{'Full Time':<14}{'Active':<10}{'Salary (£)':<14}{'Annual Leave':<15}{'Diet Preferences'}"

def update_options():
    print("\nWhat would you like to update?\n")
    print("1. First Name")
    print("2. Last Name")
    print("3. Email")
    print("4. Full Time")
    print("5. Active")
    print("6. Salary")
    print("7. Annual Leave")
    print("8. Diet Preferences\n")

def display_single_employee(employee, index):
    print("\nEmployee Details:\n")
    print_employee_details(employee, index)

def display_employees(employees):
    print("\n")
    print(get_table_headers())
    print_separator("-")
    for idx, employee in enumerate(employees, start=1):
        print(print_employee_details(employee, idx))

def main_options():
    print("\n")
    print_separator("-")
    print("Employee Management System - Main Menu")
    print_separator("-")
    print("\n1. Create Employee")
    print("2. View All Employees")
    print("3. Update Employee")
    print("4. Delete Employee")
    print("5. Exit\n")
