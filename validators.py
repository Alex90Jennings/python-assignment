import re
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
    if value not in diet_preferences:
        return False, f"Diet preference must be one of: {', '.join(diet_preferences)}."
    return True, ""

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