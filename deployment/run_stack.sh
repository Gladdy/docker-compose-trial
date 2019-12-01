#!/bin/bash
cd `dirname $0`
source activate quickshort
python ../backend/manage.py build
docker-compose build
docker-compose up