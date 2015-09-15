#!/bin/bash

LOGFILE="$HOME/external/tpo_forum.html"
CMD="python run.py db"
SLEEP="sleep 30"

FINISH_MSG="Work done. I'll sleep now."
START_MSG="Begin"

echo $(date  +"[ %Y-%m-%d %H:%M:%S.%6N ]") $START_MSG;
$CMD | tee -a $LOGFILE;
echo $(date  +"[ %Y-%m-%d %H:%M:%S.%6N ]") $FINISH_MSG;
$SLEEP;
echo ""
