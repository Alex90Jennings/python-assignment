import re
from datetime import datetime
from api import get_employee
from consts import diet_preferences

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
    if not 6 <= len(email) <= 35:
        return False, "Name must be between 6 and 35 characters long."
    if get_employee("email", email):
        return False, "Email must be unique."
    return True, ""

def is_valid_salary(value):
    is_valid, message = is_valid_positive_whole_number(value)
    if not is_valid:
        return False, message
    if float(value) < 10000:
        return False, "Part time employees must earn more than 10000."
    return True, ""

def is_valid_leave_days(value):
    is_valid, message = is_valid_positive_whole_number(value)
    if not is_valid:
        return False, message
    if float(value) < 10:
        return False, "Annual leave days should be above 10."
    if float(value) > 30:
        return False, "Annual leave days should be below 30."
    return True, ""

def is_valid_diet_preference(value):
    if value not in diet_preferences:
        return False, f"Diet preference must be one of: {', '.join(diet_preferences)}."
    return True, ""

def is_valid_boolean(value):
    if isinstance(value, bool):
        return True, ""
    return False, "Must be either 'true', 'false'"

def is_valid_date(value):
    if not value:
        return False, "Date cannot be empty or None."
    try:
        date = datetime.strptime(value, "%d/%m/%Y")
        today = datetime.today()
        if date > today:
            return False, "Date cannot be in the future."
        if date.year < 2022:
            return False, "Date cannot be before the year 2022."
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use dd/mm/yyyy."

def is_valid_positive_whole_number(value):
    try:
        num = float(value)
        if num <= 0:
            return False, "Number must be positive."
        if not num.is_integer():
            return False, "Number must be a whole number."
        return True, ""
    except ValueError:
        return False, "Value must be a number."
    
def is_valid_employee(employee):
    field_validations = {
        "firstName": is_valid_name,
        "lastName": is_valid_name,
        "isFullTime": is_valid_boolean,
        "isActive": is_valid_boolean,
        "salary": is_valid_salary,
        "annualLeaveDays": is_valid_leave_days,
        "dateJoined": is_valid_date
    }
    for field, validator in field_validations.items():
        is_valid, error_message = validator(employee.get(field))
        if not is_valid:
            print(f"Error: Employee with ID {employee.get('_id', 'unknown')} is invalid - {field}: {error_message}")
            return None
    return employee
