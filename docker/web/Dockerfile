FROM php:8.2-apache

# Instala dependencias y extensiones necesarias
RUN apt-get update && apt-get install -y libzip-dev zip unzip \
    && docker-php-ext-install pdo pdo_mysql mysqli

# Habilita módulo de reescritura de Apache (Laravel lo necesita)
RUN a2enmod rewrite


RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    libpng-dev \
    libzip-dev \
    zip \
    && curl -sL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs
# Define el nuevo DocumentRoot

# Instalar Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer



# Clonar el proyecto
RUN if [ -d /var/www/html/.git ]; then \
        cd /var/www/html && git pull; \
    else \
        git clone https://github.com/Buferxon/Laravel-Esp32.git /var/www/html; \
    fi



# Aplica el nuevo DocumentRoot en la configuración de Apache
RUN sed -ri -e 's!/var/www/html!/var/www/html/public!g' /etc/apache2/sites-available/000-default.conf \
 && sed -ri -e 's!/var/www/!/var/www/html/!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf
# Copiar archivo personalizado de configuración de Apache
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf

COPY .env /var/www/html/.env

COPY database.php /var/www/html/public/database.php

RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html/storage /var/www/html/bootstrap/cache \
    && chmod -R 755 /var/www/html/public


# Establece la carpeta del proyecto como directorio de trabajo
WORKDIR /var/www/html

# Instala las dependencias de Composer
RUN composer install


# Instala las dependencias de Node.js y construye los assets
RUN npm install 
RUN npm run build

RUN php artisan key:generate
RUN php artisan config:cache
RUN php artisan route:cache
RUN php artisan view:cache
# RUN php artisan migrate
# Ejecuta las migraciones de la base de datos
# RUN php artisan migrate --force


    