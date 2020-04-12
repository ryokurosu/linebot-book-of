#!/bin/sh

killall python
killall chromedriver
killall chrome

# export DISPLAY=:0
PROG_DIR=`dirname $0`

cd $PROG_DIR
git pull origin master

wget -P $PROG_DIR https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_mac64.zip
unzip chromedriver_mac64.zip
rm chromedriver_mac64.zip

source $PROG_DIR/env/bin/activate
nohup python3 $PROG_DIR/cron.py > $PROG_DIR/logs/`date +%Y%m%d_%H%M%S`.log &