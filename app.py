from flask import Flask, render_template, request
from api import get_employees
app = Flask(__name__)

employees = get_employees()
diet_preferences = ["Vegan", "Vegetarian", "Halal", "Kosher", "Paleo", "Gluten-Free", "Dairy-Free", "Low-Carb", "Keto"]

@app.route('/')
def main_menu():
    return render_template('main-menu.html')

@app.route('/employees_table')
def employee_table():
    return render_template('employees-table.html', employees=employees)

@app.route('/employee-details')
def employee_details():
    employee_email = request.args.get('email')
    employee = next((employee for employee in employees if employee['email'] == employee_email), None)
    if employee:
        return render_template('employee-details.html', employee=employee)
    else:
        return "employee not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
