#!/bin/sh
set -e
flask db upgrade
exec gunicorn -b 0.0.0.0:$PORT run:app