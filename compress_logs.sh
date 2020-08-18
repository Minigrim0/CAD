#!/bin/bash

LOGNAME="$(date +'%Y-%m-%d').log"
DIRNAME="$HOME/docker/apps/logs/$(date +'%Y-%m')/"
mkdir -p $DIRNAME
docker cp cad_web_1:/home/app/web/logs/cad.log $DIRNAME$LOGNAME
cd $DIRNAME
tar cf "$DIRNAME$LOGNAME.tar" $DIRNAME$LOGNAME
rm -f $DIRNAME$LOGNAME
