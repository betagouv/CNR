reset-db:
	psql -c 'DROP DATABASE cnr;'
	psql -c 'ALTER USER cnr CREATEDB;'
	psql -c 'CREATE DATABASE cnr OWNER cnr;'
	python manage.py migrate

.PHONY: web-prompt
web-prompt:
	docker-compose run --rm web bash

.PHONY: test-unit
test-unit:
	python manage.py test --settings cnr.settings_test

.PHONY: test-e2e
test-e2e:
	python manage.py behave

.PHONY: test
test: test-e2e test-unit
