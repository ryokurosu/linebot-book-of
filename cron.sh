#!/bin/sh

PROG_DIR=/home/root/app
source $PROG_DIR/bin/activate

python $PROG_DIR/cron.py
