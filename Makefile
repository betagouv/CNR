destroy-rebuild-dev-db:
	psql -c 'DROP DATABASE cnr;'
	psql -c 'CREATE DATABASE cnr OWNER cnr;'
	psql -c 'ALTER USER cnr CREATEDB;'
	python manage.py migrate
