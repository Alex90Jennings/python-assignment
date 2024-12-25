from flask import Flask, render_template
from assets import generate_user
import random

app = Flask(__name__)

@app.route('/')
def index():
    users = [generate_user() for _ in range(20)]
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
