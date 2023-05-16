# Makefile
build:
	docker compose build

dock_ident:
	docker ps -a

migrate:
	docker exec -it api_aio_test alembic revision --autogenerate -m "init"

create:
	docker exec -it api_aio_test python db_init.py

migrate_up:
	docker exec -it api_aio_test alembic upgrade head

start:
	docker compose up -d

stop:
	docker-compose stop

psql:
	docker exec -it api_aio_postgres psql -U api_user api_db


