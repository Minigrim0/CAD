if [[ "$1" == "dev" ]]; then
    export COMPOSE_PROJECT_NAME=cad-dev

    git pull
    docker-compose -f docker/docker-compose.dev.yml up -d --build
    docker-compose -f docker/docker-compose.dev.yml exec web python manage.py migrate --noinput
    docker-compose -f docker/docker-compose.dev.yml exec web python manage.py collectstatic --no-input --clear
    docker-compose -f docker/docker-compose.dev.yml restart nginx
else
    export COMPOSE_PROJECT_NAME=cad-prod

    git pull
    docker-compose -f docker/docker-compose.yml up -d --build
    docker-compose -f docker/docker-compose.yml exec web python manage.py migrate --noinput
    docker-compose -f docker/docker-compose.yml exec web python manage.py collectstatic --no-input --clear
    docker-compose -f docker/docker-compose.yml restart nginx
fi
