#!/bin/sh
set -e

poetry run alembic upgrade head
exec poetry run uvicorn --host 0.0.0.0 todolist.app:app --reload