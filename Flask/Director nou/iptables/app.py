from flask import request, jsonify, Flask, send_from_directory
import re
import os
from flask_cors import CORS
import subprocess

app = Flask(__name__)

CORS(app, resources={r"/iptables/*": {"origins": "http://20.127.44.76:5000"}})

#source retele/bin/activate =>activare mediu virtual

# Get all iptables rules
@app.route('/iptables/filter', methods=['GET'])
def get_iptables_filter():
    #result = subprocess.run(['sudo', 'iptables', '-t', 'filter', '-n', '-v' , '-L', 'INPUT', '--line-numbers'], capture_output=True, text=True)
    result = subprocess.run(['sudo', 'iptables', '-t', 'filter', '-n', '-v' , '-L', '--line-numbers'], capture_output=True, text=True) # to see all filter rules

    return jsonify({'iptables_rules': result.stdout})

@app.route('/iptables/nat', methods=['GET'])
def get_iptables_nat():
    #result = subprocess.run(['sudo', 'iptables', '-t', 'nat', '-n', '-v' , '-L',  'PREROUTING', '--line-numbers'], capture_output=True, text=True)
    result = subprocess.run(['sudo', 'iptables', '-t', 'nat', '-n', '-v' , '-L',  '--line-numbers'], capture_output=True, text=True) #to see all nat rules

    return jsonify({'iptables_rules': result.stdout})


# Add a rule to iptables
@app.route('/iptables/add', methods=['POST'])
def add_iptables_rule():
    data = request.get_json()
    rule_table = data.get('rule_table')
    rule_type = data.get('rule_type')
    rule_action = data.get('rule_action')
    ip_address = data.get('ip_address')
    ip_address_destination = data.get('ip_address_destination')
    ip_dest_final = ip_address_destination + ":80"
    port = data.get('port')

    if not rule_table or not rule_type or not rule_action or not ip_address or not port:
        return jsonify({'error': 'Invalid rule format'}), 400

    if rule_table == "nat":
        rule_command = ['sudo', 'iptables', '-t', rule_table, '-A', rule_type, '-p', 'tcp', '-d', ip_address, '--dport', port, '-j', rule_action, '--to', ip_dest_final]
    else:
        rule_command = ['sudo', 'iptables', '-A', rule_type, '-p', 'tcp', '-s', ip_address, '--dport', port, '-j', rule_action]
        print("sudo iptables -A " + rule_type + " -p tcp -s " + ip_address + " --dport " + port + " -j " + rule_action)

    subprocess.run(rule_command, capture_output=True, text=True)

    return jsonify({'message': 'Rule added successfully'})

# Delete a rule from iptables
@app.route('/iptables/delete', methods=['DELETE'])
def delete_iptables_rule():
    data = request.get_json()
    rule_type = data.get('rule_type')
    rule_number = data.get('rule_number')
    
    if not rule_type or not rule_number:
        return jsonify({'error': 'Invalid rule format'}), 400

    print("sudo iptables -D " +  rule_type + " " + rule_number)
    subprocess.run(['sudo', 'iptables', '-D', rule_type, rule_number])
    return jsonify({'message': 'Rule deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5001)