import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))
from application.utils.solve_utils import *
from flask import Flask, render_template, request, jsonify


# Create app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    payments = [float(p) for p in data['payments']]

    transactions = minimize_transactions(payments)
    return jsonify({'transactions': transactions})


if __name__ == '__main__':
    app.run(debug=True)