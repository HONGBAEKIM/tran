FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y nginx openssl dumb-init \
    && apt-get install npm -y 

COPY ./conf/default.conf /etc/nginx/conf.d/default.conf
COPY tools/docker-entrypoint.sh /docker-entrypoint.sh


RUN chmod +x /docker-entrypoint.sh

EXPOSE 443

#/usr/bin/dumb-init: simple process supervisor and init system designed to run as PID 1 (the first process) in minimal container environments. 
#It helps to ensure proper handling of signals and reaping of zombie processes.

#--: This is an argument passed to dumb-init. It signifies the end of options 
#and allows the command to follow (CMD instruction in your Dockerfile) to be treated as arguments to the dumb-init process.
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/docker-entrypoint.sh"]


# FROM debian:bullseye

# # Run package updates and install Nginx
# # openssl uses it for HTTPS
# # dumb-init is a simple process supervisor designed to run as PID 1 in minimal container environments.

# RUN apt-get update && \
#     apt-get upgrade -y && \
#     apt-get install -y nginx openssl dumb-init



# # # Check if the directory /var/www/html/dist exists
# # # -d stands for directory
# # # 101:101 represents the user ID and group ID of the nginx user and group
# # RUN [ -d /var/www/html/dist ] || mkdir -p /var/www/html/dist && \
# #     chown -R 101:101 /var/www/html/dist && \ 
# #     chmod -R 755 /var/www/html/dist


# # COPY ./conf/default.conf /etc/nginx/conf.d/default.conf
# # #COPY /tools/docker-entrypoint.sh /docker-entrypoint.sh
# # COPY ./tools/docker-entrypoint.sh /docker-entrypoint.sh

# # RUN chmod +x /docker-entrypoint.sh

# # EXPOSE 443

# # ENTRYPOINT ["/usr/bin/dumb-init", "--"]
# # CMD ["/docker-entrypoint.sh"]

# # Execute nginx
# exec nginx -g "daemon off;"