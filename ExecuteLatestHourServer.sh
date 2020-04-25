#!/bin/bash

# ----------- Date manipulation -------
currHour=`date +%H`
currDate=`date +%Y'-'%m'-'%d`
#echo $currDate

/usr/local/anaconda/bin/python /ServerScripts/LYDAR/Main.py $currDate $currHour
