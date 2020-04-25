import os
from paramiko import SSHClient
from scp import SCPClient
import time

origen= time.strftime("%Y-%m-%d")

os.chdir('/home/perfilador/data/graficas/')
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect("132.248.8.29", username="webruoa", password="P1ctur3s")
scp = SCPClient(ssh.get_transport())
scp.put(origen, recursive=True, remote_path='/var/www/html/img/perfilador/')
scp.close()
ssh.close()
