docker build -t quickshort-web -f deployment/web/Dockerfile .
docker run -d -p 8001:8001 quickshort-web
