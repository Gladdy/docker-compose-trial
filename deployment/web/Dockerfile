FROM continuumio/miniconda3:4.6.14
COPY deployment/web/requirements.txt /config/requirements.txt

RUN conda install --yes --file /config/requirements.txt -c conda-forge

COPY backend/manage.py /app/manage.py
COPY backend/quickshort /app/quickshort

ENV DJANGO_ENV=prod
ENV DOCKER_CONTAINER=1

## for now just migrate on container creation
#RUN cd app && DJANGO_ENV=prod DOCKER_CONTAINER=1 python manage.py migrate

COPY deployment/web/uwsgi.ini /config/uwsgi.ini
EXPOSE 8001


CMD uwsgi --ini /config/uwsgi.ini