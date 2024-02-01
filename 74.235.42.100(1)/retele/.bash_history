ss -tulp
netstat -tulp
ls
sudo apt install python3-pip
sudo apt update
sudo apt install python3-pip
pip install flask
python3 app.py 
sudo apt install openvpn easy-rsa
mkdir ~/easy-rsa
ln -s /usr/share/easy-rsa/* ~/easy-rsa/
sudo chown retele ~/easy-rsa
chmod 700 ~/easy-rsa
cd ~/easy-rsa
echo "set_var EASYRSA_ALGO \"ec\"" > vars
echo "set_var EASYRSA_DIGEST \"sha512\"" >> vars
set var EASYRSA_ALGO "ec"
set var EASYRSA_DIGEST "sha512"
./easyrsa init-pki
cd ~/easy-rsa
./easyrsa gen-req server nopass
sudo cp /home/retele/easy-rsa/pki/private/server.key /etc/openvpn/server/
./easyrsa build-ca
./easyrsa sign-req server server
sudo cp pki/issued/server.crt /etc/openvpn/server/
sudo cp pki/ca.crt /etc/openvpn/server/
cd ~/easy-rsa
openvpn --genkey --secret ta.key
sudo cp ta.key /etc/openvpn/server
mkdir -p ~/client-configs/keys
chmod -R 700 ~/client-configs
cd ~/easy-rsa
./easyrsa gen-req client nopass
cp pki/private/client.key ~/client-configs/keys/
./easyrsa sign-req client client
cp pki/issued/client.crt ~/client-configs/keys/
cp ~/easy-rsa/ta.key ~/client-configs/keys/
sudo cp /etc/openvpn/server/ca.crt ~/client-configs/keys/
sudo chown retele ~/client-configs/keys/*
sudo cp /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz /etc/openvpn/server/
sudo gunzip /etc/openvpn/server/server.conf.gz
sudo nano /etc/openvpn/server/server.conf
sudo nano /etc/sysctl.conf
ifconfig
sudo apt install net-tools
ifconfig
sudo nano /etc/ufw/before.rules
sudo nano /etc/default/ufw
sudo ufw allow 1194/udp
sudo ufw allow OpenSSH
sudo ufw disable
sudo ufw enable
sudo systemctl -f enable openvpn-server@server.service
sudo systemctl start openvpn-server@server.service
sudo systemctl status openvpn-server@server.service
cd ..
python3 app.py
sudo ufw disable
python3 app.py
ifconfig
python3 app.py
chmod +x generate_all.sh 
chmod +x make_config.sh 
python3 app.py
chown retele generate_all.sh 
python3 app.py
ls -l
chown root generate_all.sh 
sudo chown root generate_all.sh 
sudo chown root make_config.sh 
python3 app.py
ls -l
python3 app.py
python3 --version
pip install subproccess
096 Jan 31 11:09 Flask
-rwxr-xr-x 1 root   root   1866 Jan 20 07:33 generate_all.sh
python3 app.py
sudo apt get install expect
sudo apt-get install expect
python3 app.py
ls
cd client-configs/
ls
mkdir files
ls
cd ..
python3 app.py
mkdir -p ~/client-configs/files
cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf ~/client-configs/base.conf
sudo nano ~/client-configs/base.conf 
python3 app.py
cd /etc/openvpn
ls
sudo nano update-resolv-conf 
ls
cd server/
ls
sudo nano server.conf
cd ~
sudo systemctl restart openvpn
sudo systemctl status opencpv
sudo systemctl status openvpn
python3 app.py
cd /etc/openvpn/server/
ls
sudo nano server.conf 
cd ~
python3 app.py
