#!/bin/bash -e
cd `dirname $0`
docker-compose build
docker-compose up