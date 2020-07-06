#!/bin/bash
set -e

if [ "$FLASK_ENV" = 'DEV' ]; then
  echo "Running Development Server"
  exec python server.py

elif [ "$FLASK_ENV" = 'TEST' ]; then
  echo "Running Tests"
  echo "Retry after DB started, if too many errors"
  echo ""
  exec pytest --cov=introdon

else
  echo "Running Production Server"
  exec gunicorn server:app -c gunicorn_setting.py
fi
