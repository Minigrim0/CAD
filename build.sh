docker-compose down -v
docker-compose build
docker-compose run cad python manage.py migrate --noinput
docker-compose run cad python manage.py collectstatic --no-input --clear
