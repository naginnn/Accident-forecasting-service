FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

# Копируем файлы веб-сайта
#COPY html/ /usr/share/nginx/html