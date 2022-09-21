reset-db:
	psql -c 'DROP DATABASE cnr;'
	psql -c 'ALTER USER cnr CREATEDB;'
	psql -c 'CREATE DATABASE cnr OWNER cnr;'
	python manage.py migrate

.PHONY: web-prompt
web-prompt:
	docker-compose run --rm web bash

.PHONY: test-e2e
test-e2e:
	python manage.py behave
