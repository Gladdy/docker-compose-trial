FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
#COPY deployment/nginx/quickshort.conf /etc/nginx/conf.d/quickshort.conf
COPY deployment/nginx/uwsgi_params /etc/nginx/uwsgi_params
COPY backend/build/ /staticfiles/

EXPOSE 80
#CMD nginx-debug