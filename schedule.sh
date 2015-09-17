#!/bin/bash
shopt -s expand_aliases

export TZ='Asia/Kolkata';
export LOGDIR="$HOME/external/logs";
export LOGFILE_TXT="$LOGDIR/tpo_forum_$(date +%Y%m%d).txt";
export LOGFILE_HTML="$LOGDIR/tpo_forum_$(date +%Y%m%d).html";
export FINISH_MSG="Work done. I'll sleep now.";
export START_MSG="Begin";

alias DATE='date +"[ %Y-%m-%d %H:%M:%S.%6N ]"';
alias CMD="python run.py db";
alias SLEEP="sleep 30";
alias EXP_LOGS="cat $LOGFILE_TXT | ccze -h";

echo $(DATE) $START_MSG | tee -a $LOGFILE_TXT;
CMD | tee -a $LOGFILE_TXT;
echo $(DATE) $FINISH_MSG | tee -a $LOGFILE_TXT;
SLEEP;
echo "" | tee -a $LOGFILE_TXT;

EXP_LOGS > $LOGFILE_HTML;
