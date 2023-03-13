## Youtube clone with Django and Docker

This is a simple Youtube clone made with Django and Docker.

### How to run
1. Clone the repository
2. Run `docker-compose up -d` in the root directory
3. Run `docker-compose exec web python manage.py migrate` to migrate the database
4. Run `docker-compose exec web python manage.py createsuperuser` to create a superuser
5. Run `docker-compose exec web python manage.py collectstatic` to collect static files

The project will be available at `localhost`