#!/bin/bash
export $(grep -v '^#' /usr/local/etc/redis/config.properties | xargs)

: "$(sed -i "s/TEMPLATE_MASTER_NAME/$MASTER_USER/g" /usr/local/etc/redis/users.acl)"
: "$(sed -i "s/TEMPLATE_MASTER_PW/$REDIS_MASTER_PW/g" /usr/local/etc/redis/users.acl)"
: "$(sed -i "s/TEMPLATE_CELERY_PW/$REDIS_CELERY_PW/g" /usr/local/etc/redis/users.acl)"

redis-server /usr/local/etc/redis/redis.conf