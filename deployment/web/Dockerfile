FROM continuumio/miniconda3:4.6.14
COPY deployment/web/requirements.txt /config/requirements.txt

RUN conda install --yes --file /config/requirements.txt -c conda-forge

COPY backend/manage.py /app/manage.py
COPY backend/quickshort /app/quickshort

# for now just migrate on container creation
RUN cd app && python manage.py migrate

COPY deployment/web/uwsgi.ini /config/uwsgi.ini
EXPOSE 8001
#EXPOSE 8080



CMD uwsgi --ini /config/uwsgi.ini