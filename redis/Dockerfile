FROM redis:alpine

LABEL MAINTAINER="Abdullah Zaiter <abdu.zaiter@gmail.com>"

WORKDIR /usr/local/etc/redis/

COPY entrypoint.sh /usr/local/etc/redis/entrypoint.sh
COPY redis.conf /usr/local/etc/redis/redis.conf
COPY users.acl /usr/local/etc/redis/users.acl
COPY config.properties /usr/local/etc/redis/config.properties

RUN addgroup -S redis_config && adduser -S redis_config -G redis_config --shell /bin/sh
RUN chown -R redis_config /usr/local/etc/redis/
USER redis_config

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]