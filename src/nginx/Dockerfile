FROM nginx:1.27-alpine

COPY conf/nginx.conf /etc/nginx/nginx.conf

COPY certs /etc/nginx/certs

CMD ["nginx", "-g", "daemon off;"]