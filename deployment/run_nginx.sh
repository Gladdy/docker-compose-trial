docker build -t quickshort-nginx -f nginx/Dockerfile ..
docker run -p 8080:80 quickshort-nginx