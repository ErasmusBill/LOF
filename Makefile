.PHONY: build up down logs \
	runserver shell migrate makemigrations showmigrations \
	createsuperuser superuser collectstatic test check \
	dbshell flush

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

logs:
	docker compose logs -f

runserver:
	python manage.py runserver

shell:
	python manage.py shell

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

showmigrations:
	python manage.py showmigrations

createsuperuser:
	python manage.py createsuperuser

superuser: createsuperuser

collectstatic:
	python manage.py collectstatic --noinput

test:
	python manage.py test

check:
	python manage.py check

dbshell:
	python manage.py dbshell

flush:
	python manage.py flush --noinput
