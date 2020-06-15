echo "------------- Building the image -------------"
docker-compose build
echo "------------- Making  migrations -------------"
docker-compose run --rm cad /bin/bash -c './manage.py migrate'
echo "------------- Collecting statics -------------"
docker-compose run --rm cad /bin/bash -c './manage.py collectstatic --no-input'
