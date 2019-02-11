#inherit from apache and php7
FROM php:7.0-apache

RUN apt-get update
RUN apt-get install -y python python-pip
COPY conf/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN a2enmod rewrite
RUN a2enmod headers

COPY src/ /var/www/html/
COPY conf/headers.conf /etc/apache2/mods-enabled/
RUN chown -R www-data:www-data /var/www/html/*


#dont output the logs to stdout/stderr
RUN rm /var/log/apache2/error.log && touch /var/log/apache2/error.log
RUN rm /var/log/apache2/access.log && touch /var/log/apache2/access.log

EXPOSE 80
