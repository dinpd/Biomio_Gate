#!/bin/bash
# Make Server Certificate
domain=$1
if [ -z "$domain" ]
then
    echo "Argument not present."
    echo "Useage $0 [common name]"

    domain=127.0.0.1
fi
commonname=$domain

#Change to your company details
country=UA
state=Lviv
locality=Lviv
organization=vakoms.com.ua
organizationalunit=Vakoms
email=vakoms@gmail.com

#Optional
echo "Please, input password:"
read -s password


openssl genrsa -des3 -passout pass:$password -out server.orig.key 2048
openssl rsa -in server.orig.key -passin pass:$password -out server.key
openssl req -new -key server.key -out server.csr -passin pass:$password \
   -subj "/C=$country/ST=$state/L=$locality/O=$organization/OU=$organizationalunit/CN=$commonname/emailAddress=$email"
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
openssl x509 -in server.crt -out server.pem -outform PEM
echo "---------------------------"
echo "-----Below is your CSR-----"
echo "---------------------------"
echo
cat server.csr

echo
echo "---------------------------"
echo "-----Below is your Key-----"
echo "---------------------------"
echo
cat server.key
