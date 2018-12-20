cp nginx.conf /usr/nginx/sites-enabled/nginx.conf

cd /etc/ssl
openssl genrsa -des3 -out server.key 1024
openssl req =new -key server.key -out server.csr
cp server.key server.key.org
openssl rsa -in server.kry.org -out server.key
openssl x509 -req -days 365 -in sercer.csr -signkey server.key -out server.crt
