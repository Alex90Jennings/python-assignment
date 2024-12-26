from flask import Flask, render_template
from assets import generate_user

app = Flask(__name__)

@app.route('/')
def main_menu():
    return render_template('main-menu.html')

@app.route('/user_table')
def user_table():
    users = [generate_user() for _ in range(20)]
    return render_template('user-table.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
