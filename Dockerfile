# Використовуємо стандартний образ для Nginx
FROM nginx:alpine

# Копіюємо файли з поточної директорії в контейнер
COPY . /usr/share/nginx/html

# Відкриваємо порт 80
EXPOSE 80

COPY nginx.conf /etc/nginx/conf.d/default.conf
