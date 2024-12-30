from flask import Flask, render_template, request
from assets import generate_user

app = Flask(__name__)
users = [generate_user() for _ in range(20)]

@app.route('/')
def main_menu():
    return render_template('main-menu.html')

@app.route('/users_table')
def user_table():
    return render_template('users-table.html', users=users)

@app.route('/user-details')
def user_details():
    user_id = request.args.get('_id')
    user = next((user for user in users if user['_id'] == user_id), None)
    if user:
        return render_template('user-details.html', user=user)
    else:
        return "User not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
