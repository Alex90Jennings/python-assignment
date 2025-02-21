from consts import diet_preferences


class ReturnToMenuException(Exception):
    pass

def get_input(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() == ":menu":
        raise ReturnToMenuException
    return user_input

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

def get_new_value(update_field):
    if update_field == "dietPreferences":
        return select_diet_preferences()
    elif update_field == "isFullTime" or update_field == "isActive":
        new_value = get_input(f"Enter the new value for {update_field} (true/false): ").strip().lower()
        if new_value not in ["true", "false"]:
            print("Invalid input. Please enter 'true' or 'false'.")
            return None
        return new_value == "true"
    else:
        new_value = get_input(f"Enter the new value for {update_field}: ").strip()
        if update_field == "salary" or update_field == "annualLeaveDays":
            return round(float(new_value))
        else:
            return new_value

def select_diet_preferences():
    print("\nAvailable Diet Preferences:")
    for i, preference in enumerate(diet_preferences, start=1):
        print(f"{i}. {preference}")
    
    user_input = get_input("Enter the numbers of diet preferences (separate by commas, up to 2): ").strip()
    if user_input:
        try:
            selected_numbers = [int(num.strip()) for num in user_input.split(',')]
            if len(selected_numbers) < 0 or len(selected_numbers) > 2:
                print("You must select between 0 and 2 preferences.")
                return []
            selected_preferences = [diet_preferences[num - 1] for num in selected_numbers if 1 <= num <= len(diet_preferences)]
            return selected_preferences
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            return []
    return []