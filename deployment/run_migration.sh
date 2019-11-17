#!/bin/bash -e
docker exec -it `docker ps -f "name=deployment_web_1" --format "{{.ID}}"` /bin/bash /do_migration.sh