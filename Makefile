# Makefile
dock_build:
	docker build -t api_aio_test .

dock_run:
	docker run -d --name api_aio_test -p 5432:5432 api_aio_test

dock_ident:
	docker ps -a

migrate:
	docker exec -it api_aio_test alembic revision --autogenerate -m "init"

create:
	python init_db.py

migrate_up:
	docker exec -it api_aio_test alembic upgrade head

start:
	docker-compose up -d --build

stop:
	docker-compose stop


