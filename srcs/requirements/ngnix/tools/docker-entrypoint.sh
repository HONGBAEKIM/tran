#!/bin/bash

#Ensures the script exits immediately 
#if any command returns a non-zero status.
set -e

#Redirects Nginx logs to standard output and standard error. 
#This is useful for Docker containers since it allows logs 
#to be captured by the Docker logging system and viewed 
#with 'docker logs'.
ln -sf /dev/stdout /var/log/nginx/access.log && \
ln -sf /dev/stderr /var/log/nginx/error.log

#Creates a self-signed SSL certificate for Nginx to use for HTTPS.
mkdir -p /etc/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/nginx.key \
        -out /etc/nginx/ssl/nginx.crt \
        -subj "/C=DE/L=berlin/O=berlin/CN=nginx" \
        #silences all output from a command, both normal messages and error messages
        > /dev/null 2>&1


# Execute nginx
#This is necessary to start the Nginx server and keep the container running
exec nginx -g "daemon off;"
