git pull
docker-compose -f docker/docker-compose.yml up -d --build
docker-compose -f docker/docker-compose.yml exec web python manage.py migrate --noinput
docker-compose -f docker/docker-compose.yml exec web python manage.py collectstatic --no-input --clear
docker-compose -f docker/docker-compose.yml restart nginx
