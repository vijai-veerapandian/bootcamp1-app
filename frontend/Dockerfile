# syntax=docker/dockerfile:1.7

# Static site — no build step. nginx-unprivileged is the official non-root
# nginx image: it listens on 8080, runs as the `nginx` user (no root), and
# runs cleanly under PodSecurity "restricted".
FROM nginxinc/nginx-unprivileged:1.27-alpine

# Replace the default server block with ours (static + /api reverse proxy).
USER root
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html app.js styles.css /usr/share/nginx/html/
USER nginx

EXPOSE 8080
