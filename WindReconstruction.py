from pandas import DataFrame
from datetime import *
import matplotlib.pyplot as plt
import plotutils
import numpy as np
import os
from DataContainer import *


def windReconstruction(ftp, rootFolder, selectedDate, time, outputFolder, ymax):
    dataType = 'wind_reconstruction_data'
    # Folder options:  boundary_layer_altitude_data
    folder = rootFolder+'/'+dataType+'/'+time+'/'
    # Create output folder
    outputFolder = outputFolder+'/'+selectedDate
    try:
        os.mkdir(outputFolder)
    except:
        print('warning: folder'+outputFolder+' already exists')

    files = ftp.nlst(folder)
    # Make 'generic' outputfile
    outFile = outputFolder+'/'

    # Iterate over all the files in the current FTP folder
    for currfile in files:

        temp = currfile.rfind('/')+1;
        # Verify if the file comes from a DBS scan
        if currfile.find('DBS') != -1:

            try:
                obj = DataContainer()
                print('Using with file:' , currfile)
                ftp.retrbinary('RETR %s' % currfile, obj.readFromFTP)
                columns = ['Timestamp', 'Azimuth', 'Elevation','Range','Xwind','Ywind','Zwind',\
                            'CNR','ConfIdx']

                # Get the date from the file as a DataFrame
                data = obj.dataToArray(columns)
                # Make an average of all columns by grouped ranges
                dataByRange = data.groupby('Range').mean()
                # Get the grouped ranges values
                ranges = dataByRange.index.values

                minute = currfile.split('_')[-4].split('-')[-2]
                dateTitle =selectedDate +' '+ time.split('-')[-2] + ':' + minute

                # ------- Plot CNR vel ------
                finalOutputFile = outFile+'CNR_'+currfile[temp:].replace('csv','png')
                plt.plot(dataByRange['CNR'],ranges)
                plt.ylim(0, 2000)
                plt.xlabel('CNR')
                plt.ylabel('m')
                plt.title(dateTitle)      
                plt.savefig(finalOutputFile)
                plt.close()

                # ------- Plot X,Y,Z vel ------
                finalOutputFile = outFile+'Allvel_'+currfile[temp:].replace('csv','png') 
                plt.plot(dataByRange['Xwind'],ranges,label='X-Wind') 
                plt.plot(dataByRange['Ywind'],ranges,label='Y-Wind') 
                plt.plot(dataByRange['Zwind'],ranges,label='Z-Wind') 
                plt.ylim(0, 2000)
                plt.xlabel('m/s')
                plt.ylabel('m')
                plt.ylim([0,ymax])
                plt.legend(loc='best')
                plt.title('All winds:'+dateTitle)
                plt.savefig(finalOutputFile)
                plt.close()

                # ------- Plot Wind Magnitude ------
                finalOutputFile = outFile+'Magnitude_'+currfile[temp:].replace('csv','png')
                windMagnitude = np.sqrt(np.square(dataByRange['Xwind'])+np.square(dataByRange['Ywind'])+ np.square(dataByRange['Zwind']))
                plt.plot(windMagnitude,ranges)
                plt.ylim(0, 2000)
                plt.xlabel('m/s') 
                plt.ylabel('m')
                plt.title('Wind magnitude :'+dateTitle)
                plt.ylim([0,ymax])
                plt.savefig(finalOutputFile)
                plt.close()
            except Exception as e:
                print("Problema calculando Wind Reconstruction", e)

