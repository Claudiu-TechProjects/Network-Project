from flask import request, jsonify, Flask, send_from_directory
import re
import os
from flask_cors import CORS
import subprocess

app = Flask(__name__)

CORS(app, resources={r"/iptables/*": {"origins": "http://20.127.44.76:5000"}})

#source retele/bin/activate =>activare mediu virtual

def add_ufw_before_rule(src_ip, dst_ip, action):

    section_start = "#REGULILE MELE\n"

    # Read the current contents of the file
    with open('/etc/ufw/before.rules', 'r') as file:
        lines = file.readlines()
    print(lines)
    # Find the index of the section start
    try:
        index = lines.index(section_start)
    except ValueError:
        raise Exception("The specified section start could not be found in before.rules")

    # Define the new rule to add
    rule = f"# Rule added via API\n-A ufw-before-forward -s {src_ip} -d {dst_ip} -j {action}\n"

    # Insert the new rule before the section start
    lines.insert(index, rule)

    # Write the updated contents back to the file
    with open('/etc/ufw/before.rules', 'w') as file:
        file.writelines(lines)

    # Reload UFW to apply changes
    subprocess.run(['sudo', 'ufw', 'reload'], capture_output=True, text=True)



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
    rule_comment = data.get('comment', 'Added via API')
    rule_action = data.get('rule_action')
    ip_address = data.get('ip_address')
    ip_address_destination = data.get('ip_address_destination', '')
    port = data.get('port')
    
    

    add_ufw_before_rule('10.8.0.0/8',ip_address,rule_action)

    # Reload UFW to apply changes
   

    return jsonify({'message': 'Rule added to before.rules and UFW reloaded'})

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