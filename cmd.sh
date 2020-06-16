#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
  echo "Running Development Server"
  exec python "server.py"
elif [ "$ENV" = 'UNIT' ]; then
  echo "Running Unit Tests"
  exec python "tests_introdon.py"
else
  echo "Running Production Server"
  exec uwsgi --ini uwsgi.ini
fi
