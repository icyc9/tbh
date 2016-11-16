#!/usr/bin/env bash

NAME="tbhapi"
APPDIR=$APPDIR
export PORT=8080

echo "Starting $NAME"

# Start your gunicorn
#exec gunicorn run -b 0.0.0.0:$PORT \
#  --name $NAME \
#  --workers $NUM_WORKERS \
#  --user=$USER --group=$GROUP \

#gunicorn run:application -b 0.0.0.0:$PORT   --name $NAME   --workers $NUM_WORKERS
gunicorn -k tornado -b 0.0.0.0:$PORT -w 4 run:application