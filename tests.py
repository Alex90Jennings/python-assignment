import pytest
from validators import (
    is_valid_name,
    is_valid_email,
    is_valid_salary,
    is_valid_leave_days,
    is_valid_diet_preference,
    is_valid_boolean,
    is_valid_date,
    is_valid_positive_whole_number
)

def mock_get_employee(field, value):
    if field == "email" and value == "existing@example.com":
        return True
    return False
@pytest.fixture(autouse=True)
def patch_get_employee(monkeypatch):
    monkeypatch.setattr("validators.get_employee", mock_get_employee)

@pytest.mark.parametrize("name, expected", [
    ("John", (True, "")),
    ("J@hn", (False, "Name must contain only letters.")),
    ("John123", (False, "Name must contain only letters.")),
    ("12345", (False, "Name must contain only letters.")),
    ("J", (False, "Name must be between 2 and 15 characters long.")),
    ("JonathanAndrewSmith", (False, "Name must be between 2 and 15 characters long.")), 
])
def test_is_valid_name(name, expected):
    assert is_valid_name(name) == expected

@pytest.mark.parametrize("email, expected", [
    ("test@example.com", (True, "")),
    ("invalid-email", (False, "Invalid email format.")),
    ("existing@example.com", (False, "Email must be unique.")),
])
def test_is_valid_email(email, expected):
    assert is_valid_email(email) == expected

@pytest.mark.parametrize("salary, expected", [
    (15000, (True, "")),
    ("15000", (True, "")),
    (9000, (False, "Part time employees must earn more than 10000.")),
    ("9000", (False, "Part time employees must earn more than 10000.")),
    ("invalid", (False, "Value must be a number.")),
])
def test_is_valid_salary(salary, expected):
    assert is_valid_salary(salary) == expected

@pytest.mark.parametrize("leave_days, expected", [
    (20, (True, "")),
    ("20", (True, "")),
    (5, (False, "Annual leave days should be above 10.")),
    ("5", (False, "Annual leave days should be above 10.")),
    (35, (False, "Annual leave days should be below 30.")),
    ("35", (False, "Annual leave days should be below 30.")),
    ("invalid", (False, "Value must be a number.")),
])
def test_is_valid_leave_days(leave_days, expected):
    assert is_valid_leave_days(leave_days) == expected

@pytest.mark.parametrize("diet, expected", [
    ("Vegetarian", (True, "")),
    ("Carnivore", (False, "Diet preference must be one of: Vegan, Vegetarian, Halal, Kosher, Paleo, Gluten-Free, Dairy-Free, Low-Carb, Keto.")),
])
def test_is_valid_diet_preference(diet, expected):
    result = is_valid_diet_preference(diet)
    assert result == expected, f"Failed for diet: {diet}, got {result}"

@pytest.mark.parametrize("value, expected", [
    (True, (True, "")),
    (False, (True, "")),
    ("true", (False, "Must be either 'true', 'false'")),
    ("false", (False, "Must be either 'true', 'false'")),
])
def test_is_valid_boolean(value, expected):
    assert is_valid_boolean(value) == expected

@pytest.mark.parametrize("date_str, expected", [
    ("10/03/2023", (True, "")),
    ("2023-03-10", (False, "Invalid date format. Use dd/mm/yyyy.")),
    ("10/03/2026", (False, "Date cannot be in the future.")),
    ("", (False, "Date cannot be empty or None.")),
    ("32/03/2023", (False, "Invalid date format. Use dd/mm/yyyy.")),
    ("10/13/2023", (False, "Invalid date format. Use dd/mm/yyyy.")),
])
def test_is_valid_date(date_str, expected):
    assert is_valid_date(date_str) == expected

@pytest.mark.parametrize("value, expected", [
    (10, (True, "")),
    ("10", (True, "")),
    (-5, (False, "Number must be positive.")),
    ("-5", (False, "Number must be positive.")),
    (3.5, (False, "Number must be a whole number.")),
    ("3.5", (False, "Number must be a whole number.")),
    ("abc", (False, "Value must be a number.")),
])
def test_is_valid_positive_whole_number(value, expected):
    assert is_valid_positive_whole_number(value) == expected
