# Network-Project

Config OPENVPN-SERVER

bash:

sudo apt update

Install OpenVPN and easy-rsa.
sudo apt install openvpn easy-rsa
mkdir ~/easy-rsa
ln -s /usr/share/easy-rsa/* ~/easy-rsa/

SET PERMISION for directory

sudo chown <user> ~/easy-rsa
chmod 700 ~/easy-rsa


cd ~/easy-rsa
echo "set_var EASYRSA_ALGO \"ec\"" > vars
echo "set_var EASYRSA_DIGEST \"sha512\"" >> vars

set var EASYRSA_ALGO "ec"
set var EASYRSA_DIGEST "sha512"

./easyrsa init-pki

cd ~/easy-rsa
./easyrsa gen-req server nopass
sudo cp /home/mehigh/easy-rsa/pki/private/server.key /etc/openvpn/server/

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
sudo chown <user> ~/client-configs/keys/*


sudo cp /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz /etc/openvpn/server/
sudo gunzip /etc/openvpn/server/server.conf.gz

Modify /etc/openvpn/server/server.conf:

;tls-auth ta.key 0 # This file is secret
tls-crypt ta.key


;cipher AES-256-CBC
cipher AES-256-GCM
auth SHA256


;dh dh2048.pem
dh none

push "redirect-gateway def1"

push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"


client-to-client

user nobody
group nogroup

Modify  /etc/sysctl.conf:

net.ipv4.ip_forward = 1

Modify  /etc/ufw/before.rules:

Put it in the end of the file

# START OPENVPN RULES
# NAT table rules
*nat
:POSTROUTING ACCEPT [0:0]
# Allow traffic from OpenVPN client to eth0 (change to the interface you discovered! , ifconfig command)
-A POSTROUTING -s 10.8.0.0/8 -o ens33 -j MASQUERADE
COMMIT
# END OPENVPN RULE

Modify  /etc/default/ufw:
DEFAULT_FORWARD_POLICY="ACCEPT"


sudo ufw allow 1194/udp
sudo ufw allow OpenSSH
sudo ufw disable
sudo ufw enable

Start OpenVPN

sudo systemctl -f enable openvpn-server@server.service
sudo systemctl start openvpn-server@server.service

sudo systemctl status openvpn-server@server.service


mkdir -p ~/client-configs/files
cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf ~/client-configs/base.conf



remote <ip> 1194
proto udp
user nobody
group nogroup
;ca ca.crt
;cert client.crt
;key client.key
;tls-auth ta.key 1
cipher AES-256-GCM
auth SHA256

redirect-gateway def1


ADD this:

key-direction 1
; script-security 2
; up /etc/openvpn/update-resolv-conf
; down /etc/openvpn/update-resolv-conf

; script-security 2
; up /etc/openvpn/update-systemd-resolved
; down /etc/openvpn/update-systemd-resolved
; down-pre
; dhcp-option DOMAIN-ROUTE .


If you want a vpn profile you can run the server flask and add your username

Commands in bash:

nano ~/client-configs/make_config.sh
#!/bin/bash
KEY_DIR=~/client-configs/keys
OUTPUT_DIR=~/client-configs/files
BASE_CONFIG=~/client-configs/base.conf
cat ${BASE_CONFIG} \
    <(echo -e '<ca>') \
    ${KEY_DIR}/ca.crt \
    <(echo -e '</ca>\n<cert>') \
    ${KEY_DIR}/${1}.crt \
    <(echo -e '</cert>\n<key>') \
    ${KEY_DIR}/${1}.key \
    <(echo -e '</key>\n<tls-crypt>') \
    ${KEY_DIR}/ta.key \
    <(echo -e '</tls-crypt>') \
    > ${OUTPUT_DIR}/${1}.ovpn

chmod 700 ~/client-configs/make_config.sh
cd ~/client-configs
./make_config.sh client