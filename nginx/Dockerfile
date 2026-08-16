FROM nginx:1.25-alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy static website files
COPY index.html  /usr/share/nginx/html/
COPY style.css   /usr/share/nginx/html/
COPY script.js   /usr/share/nginx/html/
COPY images/     /usr/share/nginx/html/images/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost/index.html || exit 1
