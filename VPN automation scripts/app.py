from flask import Flask, request, render_template, send_file
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_vpn', methods=['POST'])
def generate_vpn():
    username = request.form['username']
    process = subprocess.Popen(['./generate_all.sh', username, "1234"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(stderr.decode())
        return "A apărut o eroare la generarea profilului VPN", 500

    vpn_profile_path="/home/claudiu/client-configs/files/"+username+".ovpn"
    print(vpn_profile_path)
    return send_file(vpn_profile_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)