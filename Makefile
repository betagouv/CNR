reset-db:
	psql -c 'DROP DATABASE cnr;'
	psql -c 'ALTER USER cnr CREATEDB;'
	psql -c 'CREATE DATABASE cnr OWNER cnr;'
	python manage.py migrate
