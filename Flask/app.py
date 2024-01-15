from flask import request, jsonify, Flask
from flask_cors import CORS
import re
import os
import subprocess

app = Flask(__name__)
CORS(app)


# Get all iptables rules
@app.route('/iptables', methods=['GET'])
def get_iptables():
    result = subprocess.run(['sudo', 'iptables', '-L', '-n', '-v'], capture_output=True, text=True)
    return jsonify({'iptables_rules': result.stdout})

# Add a rule to iptables
@app.route('/iptables/add', methods=['POST'])
def add_iptables_rule():
    data = request.get_json()
    rule = data.get('rule')
    if not rule:
        return jsonify({'error': 'Invalid rule format'}), 400

    subprocess.run(['sudo', 'iptables', '-A', rule])
    return jsonify({'message': 'Rule added successfully'})

# Delete a rule from iptables
@app.route('/iptables/delete', methods=['DELETE'])
def delete_iptables_rule():
    data = request.get_json()
    rule_type = data.get('rule_type')
    rule_number = data.get('rule_number')
    
    if not rule_type or not rule_number:
        return jsonify({'error': 'Invalid rule format'}), 400

    subprocess.run(['sudo', 'iptables', '-D', rule_type, rule_number])
    return jsonify({'message': 'Rule deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)