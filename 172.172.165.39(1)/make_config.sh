#!/bin/bash
KEY_DIR=/home/retele/client-configs/keys
OUTPUT_DIR=/home/retele/client-configs/files
BASE_CONFIG=/home/retele/client-configs/base.conf

touch ${OUTPUT_DIR}/${1}.ovpn 

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