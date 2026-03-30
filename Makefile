.PHONY: build up down logs \
	runserver shell migrate makemigrations showmigrations \
	createsuperuser superuser collectstatic test check \
	dbshell flush

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

# --- Commands that now run INSIDE Docker ---

shell:
	docker compose exec web python manage.py shell

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

showmigrations:
	docker compose exec web python manage.py showmigrations

createsuperuser:
	docker compose exec web python manage.py createsuperuser

superuser: createsuperuser

collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

test:
	docker compose exec web python manage.py test

check:
	docker compose exec web python manage.py check

dbshell:
	docker compose exec web python manage.py dbshell

flush:
	docker compose exec web python manage.py flush --noinput
