#!/usr/bin/env bash

NAME="tbhapi"
APPDIR=$APPDIR
PORT=$PORT
NUM_WORKERS=$WORKERS

echo "Starting $NAME"

# Start your gunicorn
exec gunicorn tbh:app -b 0.0.0.0:PORT \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \