#!/bin/sh

killall python
killall chromedriver
killall chrome

export DISPLAY=:0
PROG_DIR=/home/root/app

cd $PROG_DIR
git fetch
git reset --hard origin/master

source $PROG_DIR/env/bin/activate

python $PROG_DIR/cron.py &
