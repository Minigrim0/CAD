#!/bin/bash

LOGNAME="$(date +'%Y-%m-%d').log"
DIRNAME="../logs/$(date +'%Y-%m')/"
mkdir -p $DIRNAME
mv logs/cad.log ../logs/$DIRNAME/$LOGNAME
cd $DIRNAME
tar cf "$LOGNAME.tar" $LOGNAME
rm -f $LOGNAME
