FROM php:7.4-apache

RUN apt-get update && \
    apt-get install -y libzip-dev && \
    docker-php-ext-install zip

RUN a2enmod rewrite

RUN mkdir -p /var/www/html/uploads && \
    chmod -R 777 /var/www/html

RUN echo "upload_max_filesize = 10M" >> /usr/local/etc/php/php.ini && \
    echo "post_max_size = 10M" >> /usr/local/etc/php/php.ini && \
    echo "display_errors = On" >> /usr/local/etc/php/php.ini

COPY index.php /var/www/html/

EXPOSE 80
