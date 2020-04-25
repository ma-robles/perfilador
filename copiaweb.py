from ftplib import FTP
from datetime import *
import os, sys, getopt

host = '132.248.8.31'
port = 21
inputFolder = '/perfilador/'  # Folder inside the FTP
outputFolder = '/home/perfilador/export/graficas'
ftp = FTP() 
ftp.connect(host,port)

# This function MUST receive a date in the format 'YYYY-MM-DD' and a Time in the format 0-24
if __name__ == "__main__":

    allArguments = sys.argv[1:]
    if len(allArguments) < 2:
        selectedDate = '2017-12-01'
        times = ['00-00','11-00']
    else:
        selectedDate = allArguments[0]
        hour = int(allArguments[1])
        times = ['%.2d-00' % hour]

    # Login into the FTP server
    print(ftp.login())

    rootFolder = inputFolder+selectedDate
    for currFolder in times: 
        time = currFolder.split('/')[-1]
        radialWindData(ftp, rootFolder, selectedDate, time, outputFolder)
        windReconstruction(ftp, rootFolder, selectedDate, time, outputFolder, 2100)

    boundaryLayer(ftp, rootFolder,  selectedDate, outputFolder)

    ftp.quit()
