#!/bin/sh

PROG_DIR=`dirname $0`

cd $PROG_DIR
git add .
git commit -m "fix: in command"
git push
