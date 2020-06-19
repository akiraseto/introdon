#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
  echo "Running Development Server"
  exec python server.py
elif [ "$ENV" = 'TEST' ]; then
  echo "Running Unit Tests"
  exec python test_introdon.py
else
  echo "Running Production Server"
  exec gunicorn server:app -c gunicorn_setting.py
fi
