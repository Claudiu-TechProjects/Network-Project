#!/usr/bin/expect -f

if {[llength $argv] != 2} {
    puts "Error: Please provide a username and common name as arguments."
    exit 1
}

set username [lindex $argv 0]
set password [lindex $argv 1]

set client_configs_dir "$env(HOME)/client-configs/keys"
set easy_rsa_dir "$env(HOME)/easy-rsa"

# Generate RSA keys and certificates for the client
exec mkdir -p $client_configs_dir
exec chmod -R 700 $client_configs_dir
cd $easy_rsa_dir

# Generate the private key and certificate request
puts "Generating private key and certificate request..."
spawn ./easyrsa gen-req $username nopass

expect {
    "Confirm key overwrite:" {send "yes\r"; exp_continue}
    "Common Name (eg: your user, host, or server name) \\\[$username\\\]:" {send "\r"; exp_continue}
}

# Check if key generation was successful
if {[catch wait] != 0} {
    puts "Error: Key generation failed."
    exit 1
}

# Copy the private key to the client-configs directory
exec cp pki/private/$username.key $client_configs_dir/

# Sign the client request
puts "Signing the certificate request..."
spawn ./easyrsa sign-req client $username

expect {
    "Confirm request details:" {send "yes\r"; exp_continue}
    "Enter pass phrase for $easy_rsa_dir/pki/private/ca.key:" {send "$password\r"; exp_continue}
}

# Check if signing was successful
if {[catch wait] != 0} {
    puts "Error: Certificate signing failed."
    exit 1
}

# Copy necessary files
exec cp pki/issued/$username.crt $client_configs_dir/
exec cp $easy_rsa_dir/ta.key $client_configs_dir/
exec sudo cp /etc/openvpn/server/ca.crt $client_configs_dir/

exec sudo chown $env(USER) $client_configs_dir/$username.crt

exec sudo chown $env(USER) $client_configs_dir/$username.key

puts "RSA keys and certificates generated successfully."

# create config file
exec /home/retele/make_config.sh $username

puts "Successfully created config file."
