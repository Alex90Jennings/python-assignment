# Software Engineering Fundamentals - (QAC020C125AW)

## Welcome to the Software Engineering Fundamentals Assignment

In order to run the console application, enter into the root folder and run:

```bash
python app.py
```

At any time in the application, typing :menu will return the user to the main menu

Pressing control + c can also exit the application gracefully without error

## What is the application?

The application is a tool for managing the staff at a company. Each employee has the following attributes:

```
First Name: A string of between 2 and 15 characters.
Last Name: A string of between 2 and 15 characters.
Email: A string of a valid email address format between 6 and 35 characters.
Is Full Time: A boolean value.
Is Active: A boolean value, which is always true for newly created employees.
Salary: A positive whole number above 10,000.
Annual Leave Days: A positive whole number between 10 and 30.
Date Joined: Date in the format dd/mm/yyyy, which is always today's date for newly created employee, must be between 2022 and today's date
Diet Preferences: A list of between 0 and 2 pre-defined possible diet preferences.
```

The application has CRUD operations to a database hosted on mongo db.

## Testing

Run 

```bash
pytest -v tests.py 
```

in order to execute the pytest testing suite unit tests of the input validators
