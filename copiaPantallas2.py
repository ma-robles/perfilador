import os
from paramiko import SSHClient
from scp import SCPClient
import time
from datetime import datetime, timedelta


date = datetime.now().strftime('%Y-%m-%d')
#yest = timedelta(days=1)
#hoy = date - yest
#date = hoy.strftime('%Y-%m-%d')
print(date)
filename = ('timeseries_daily_'+date+'.png')

os.chdir('/home/perfilador/data/graficas2/'+date+'/')
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect("132.248.8.29", username="webruoa", password="P1ctur3s")
scp = SCPClient(ssh.get_transport())
scp.put(filename, remote_path='/var/www/html/pantallas/')
scp.close()
ssh.close()
