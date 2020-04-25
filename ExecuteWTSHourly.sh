#!/bin/bash

cd /home/perfilador/perfila/

#currHour=`date +%H`
currDate=`date +%Y'-'%m'-'%d`
currHour=`date +%H`

echo python3 MainHourly.py $currDate $currHour
#/home/perfilador/anaconda2/envs/py37/bin/python3 MainHourly.py $currDate $currHour
/opt/anaconda3/bin/python3.6 MainHourly.py $currDate $currHour

#/home/perfilador/anaconda2/envs/py37/bin/python3 copiaPantallas2.py  
