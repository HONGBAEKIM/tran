FROM debian:bullseye

# Run package updates and install Nginx
# openssl uses it for HTTPS
# dumb-init is a simple process supervisor designed to run as PID 1 in minimal container environments.

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y nginx openssl dumb-init

COPY ./conf/default.conf /etc/nginx/conf.d/default.conf
#COPY /tools/docker-entrypoint.sh /docker-entrypoint.sh
COPY ./tools/docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

EXPOSE 443

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/docker-entrypoint.sh"]