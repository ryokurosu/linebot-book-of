#!/bin/sh

killall python
killall chromedriver
killall chrome

export DISPLAY=:0
PROG_DIR=/home/root/app

cd $PROG_DIR
git stash
git stash clear
git fetch
git reset --hard origin/master

source $PROG_DIR/env/bin/activate

python $PROG_DIR/cron.py > $PROG_DIR/logs/`date +%Y%m%d_%H%M%S`.log
