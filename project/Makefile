PROJECT_NAME = quizzapp


run:
	python3 manage.py runserver


clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

delete_migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

dropdb:
	rm -f db.sqlite3

resetdb: dropdb delete_migrations migrate

createsuperuser:
	python3 manage.py createsuperuser

populate:
	python3 manage.py populate