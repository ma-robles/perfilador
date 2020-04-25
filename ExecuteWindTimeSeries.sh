#!/bin/bash

cd /home/perfilador/perfila/

#currHour=`date +%H`
currDate=`date +%Y'-'%m'-'%d -d "yesterday"`
#currDate=`date +%Y'-'%m'-'%d`

echo python3 MainDaily.py $currDate
/home/perfilador/anaconda2/envs/py37/bin/python3 MainDaily.py $currDate
#/opt/anaconda3/bin/python3.6 MainDaily.py $currDate
/home/perfilador/anaconda2/envs/py37/bin/python3 copiaPantallas2.py
