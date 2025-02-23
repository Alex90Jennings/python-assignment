from consts import diet_preferences
from validators import is_valid_date, is_valid_email, is_valid_leave_days, is_valid_name, is_valid_salary

class ReturnToMenuException(Exception):
    pass

def get_input(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() == ":menu":
        raise ReturnToMenuException
    return user_input

def get_valid_input(prompt, validation_func):
    while True:
        value = get_input(prompt).strip()
        is_valid, error_msg = validation_func(value)
        if is_valid:
            return value
        print(error_msg)

def get_valid_choice(prompt, choices):
    while True:
        choice = get_input(prompt).strip().lower()
        if choice in choices:
            return choice
        print(f"Invalid input. Please enter one of {' or '.join(choices)}.")

def get_valid_index(prompt, items):
    while True:
        try:
            index = int(get_input(prompt)) - 1
            if 0 <= index < len(items):
                return index
            print("Invalid index. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def map_update_choice_to_field(choice):
    field_map = {
        "1": "firstName",
        "2": "lastName",
        "3": "email",
        "4": "isFullTime",
        "5": "isActive",
        "6": "salary",
        "7": "annualLeaveDays",
        "8": "dateJoined",
        "9": "dietPreferences"
    }
    return field_map.get(choice)

def updated_value(update_field):
    if update_field == "dietPreferences":
        return select_diet_preferences()
    
    if update_field == "dateJoined":
        return select_date_joined()

    if update_field in ["isFullTime", "isActive"]:
        return get_valid_choice(f"Enter the new value for {update_field} (true/false): ", ["true", "false"]) == "true"

    if update_field in ["salary", "annualLeaveDays"]:
        validation_func = is_valid_salary if update_field == "salary" else is_valid_leave_days
        prompt = f"Enter the new value for {update_field.replace('annualLeaveDays', 'annual leave days')}: "
        return get_valid_input(prompt.strip(), validation_func)

    validation_func = is_valid_email if update_field == "email" else is_valid_name
    return get_valid_input((f"Enter the new value for {update_field}: ").strip(), validation_func)

def select_diet_preferences():
    print("\nAvailable Diet Preferences:")
    for i, preference in enumerate(diet_preferences, start=1):
        print(f"{i}. {preference}")

    while True:
        user_input = get_input("Enter the numbers of diet preferences (separate by commas, up to 2): ").strip()
        if not user_input:
            return []
        try:
            selected_numbers = [int(num.strip()) for num in user_input.split(',')]
            if not (0 <= len(selected_numbers) <= 2):
                print("You must select between 0 and 2 preferences.")
                continue
            if any(num < 1 or num > len(diet_preferences) for num in selected_numbers):
                print("One or more selected numbers are out of range. Please try again.")
                continue
            if len(selected_numbers) == 2 and selected_numbers[0] == selected_numbers[1]:
                print("You cannot select the same preference twice. Please try again.")
                continue
            return [diet_preferences[num - 1] for num in selected_numbers]
        except ValueError:
            print("Invalid input. Please enter valid numbers, separated by commas.")

def select_date_joined():
    while True:
        date_input = input("Enter the new date joined (dd/mm/yyyy): ").strip()
        is_valid, message = is_valid_date(date_input)
        if is_valid:
            return date_input
        print(f"Invalid date. {message} Please try again.")