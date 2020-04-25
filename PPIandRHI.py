from datetime import *
import matplotlib.pyplot as plt
import plotutils
import os
from DataContainer import *

def radialWindData(ftp, rootfolder, selectedDate, time, outputFolder):
    """ This function reads the radial wind data of the selected time
    and create the images for the specified time. The images are
    for the RHI and PPI scans"""
    # Folder options:  boundary_layer_altitude_data
    folder = rootfolder+'/'+'radial_wind_data'+'/'+time+'/'
    print("In folder ",folder)
    # Create output folder
    outputFolder = outputFolder+'/'+selectedDate
    try:
        os.mkdir(outputFolder)
    except:
        print('WARNING: folder '+outputFolder+' already exists')

    files = ftp.nlst(folder)
    #print(files)
    # Make 'generic' outputfile
    outFile = outputFolder+'/'

    # Iterate over all the files in the current FTP folder
    for currfile in files:
        temp = currfile.rfind('/')+1;
        finalOutputFile = outFile+currfile[temp:].replace('csv','png')

        # Verfiy we are interested in the current file
        if currfile.find('PPI') != -1 or currfile.find('RHI') != -1 :

            try:
                # Initialize the required container
                obj = DataContainer()
                print('Using with file:' , currfile)
                ftp.retrbinary('RETR %s' % currfile, obj.readFromFTP)
                columns = ['Timestamp','ConfiID','ScanID','LOSID','Azimuth', \
                                   'Elevation','Range','RWS','DRWS','CNR']
                data = obj.dataToArray(columns)

                # Verify if the file comes from a PPI scan
                if currfile.find('PPI') != -1:
                    t1 = currfile.split('/')[-1]
                    t1 = t1.split('_')
                    title = t1[4] + " " +  t1[5].replace('-',':')
                    plt = plotutils.plot_polar_scatter(data['RWS'],  data['Range'],data['Azimuth'], "N", title, -30, 30)

                # Verify if the file comes from a PPI scan
                if currfile.find('RHI') != -1:
                    t1 = currfile.split('/')[-1]
                    t1 = t1.split('_')
                    title = t1[4] + " " +  t1[5].replace('-',':')
                    obj.fixForRHI()
                    plt = plotutils.plot_polar_scatter(data['RWS'],  data['Range'],data['Elevation'], "W", title, -30, 30)

                #plt.show()
                plt.savefig(finalOutputFile)
                plt.close()
            except Exception as e:
                print("Problema calculando radialWInd: ", e)
