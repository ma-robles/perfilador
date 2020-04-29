#!/bin/bash

# ----------- Date manipulation -------

#cd  /home/perfilador/perfila/
currHour=`date +%H`
currDate=`date +%Y'-'%m'-'%d`
#echo $currDate

echo python Main.py $currDate $currHour
python Main.py $currDate $currHour

python2.7  copiaweb2.py

