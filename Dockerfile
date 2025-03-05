# Використовуємо стандартний образ для Nginx
FROM nginx:alpine

# Копіюємо файли сайту
COPY . /usr/share/nginx/html

# Копіюємо конфігурацію Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Відкриваємо порт 80
EXPOSE 80

