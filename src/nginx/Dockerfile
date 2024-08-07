FROM nginx:1.27-alpine

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

COPY ./cert /etc/nginx/cert

EXPOSE 80/tcp

CMD ["nginx", "-g", "daemon off;"]