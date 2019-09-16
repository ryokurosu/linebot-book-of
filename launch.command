#!/bin/sh

PROG_DIR=`dirname $0`

cd $PROG_DIR
source $PROG_DIR/env/bin/activate
pip3 install -r requirements.txt