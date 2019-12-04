#!/bin/bash
export $(cat .env | xargs)
source activate quickshort
python ../backend/manage.py build
docker-compose build
docker-compose up