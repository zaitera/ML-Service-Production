FROM python:3.9-slim-buster

LABEL MAINTAINER="Abdullah Zaiter <a.zaiter@penguinin.com>"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD . /var/www/
RUN pip install -r ./requirements.txt

RUN addgroup --gid $GROUP_ID www
RUN adduser -disabled-password -u $USER_ID --gid $GROUP_ID www --shell /bin/sh
RUN chown -R www /var/www/
USER www

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]
