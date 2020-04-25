from ftplib import FTP
from datetime import *
import matplotlib.pyplot as plt
import plotutils
import numpy as np
import os
import re
from DataContainer import *

def boundaryLayer(ftp, rootFolder, selectedDate, outputFolder):
    """ Reads and plots the boundary layer during the time of the selected date"""
    dataType = 'boundary_layer_altitude_data'
    # Folder options:  boundary_layer_altitude_data
    inputFolder = rootFolder+'/'+dataType
    # Create output inputFolder
    outputFolder = outputFolder+'/'+selectedDate
    try:
        os.mkdir(outputFolder)
    except:
        print('warning: inputFolder'+outputFolder+' already exists')

    outFile = outputFolder+'/'
    folders = ftp.nlst(inputFolder)
    dataContainer = DataContainer()
    times = []

    # Create regular expression to validate folder names to 00-00, 01-00 etc
    regExpHour = re.compile('[0-9]{2}') # Match exactly 2 numbers
    regExpCSV = re.compile('.*\.csv') # Match exactly csv files
    for currFolder in folders:
        hour = 'NONE'
        try:
            hour = currFolder.split('/')[-1].split('-')[-2]
        except:
            print('warning: This folder is not a time'+currFolder)

        if regExpHour.match(hour):
            times.append(hour) 
            # Read files for this folder
            files = ftp.nlst(currFolder)
            #print("list of files:",files)
            # For each folder we need to read the files and save the data
            for currfile in files:
                if regExpCSV.match(currfile):
                    ftp.retrbinary('RETR %s' % currfile, dataContainer.readFromFTP)
                    #print('Working with file:' , currfile)
                    columns = ['Timestamp','ConfiID','ScanID','LayerID','Azimuth', \
                                       'Elevation','RLA','MLA']

                    # Decide if we intialize the data or append from new file
                    data = dataContainer.dataToArray(columns,True)
                    dataContainer.clearString()

    #print(times)
    # ------- Plot CNR vel ------
    finalOutputFile = outFile+'RLA_'+selectedDate+'_.png'
    plt.scatter(times,data['RLA'],label='Residual')
    plt.scatter(times,data['MLA'],label='Mixing')
#original olmo era con .plot aca arriba    
    plt.xlabel('Time') 
    plt.ylabel('m')
    plt.legend(loc='best')
    plt.title(selectedDate)
    plt.savefig(finalOutputFile)
    plt.close()
