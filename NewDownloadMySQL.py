import sys, string
import csv
__author__="Olmo S. Zavala Romero"

import MySQLdb
import numpy as np
from pandas import DataFrame,Series
from datetime import date
from datetime import timedelta

def writeToFile(fileName, data, mode):
    """ Writes 'data' to a file name. mode it can be 'a' or 'w' to appendo or write """
    f = open(fileName,mode)
    if mode == "a":
        f.write('\n')
    f.write(data)

def nameFromPath(filePath):
    """Obtains the file name from a path"""
    indx = filePath.rindex('/')
    name = filePath[indx+1:len(filePath)]
    return name

def makeConn():
    #For Posgresql only
    conn = MySQLdb.connect(host="10.20.9.108", user="download", passwd="d0wnl0ad", db="lidar")
    return conn

def helperIterateFunction(conn, currDay, endDay, folder, fileName, storeProc, cols):

    endDate = endDay.strftime('%Y-%m-%d')
    while currDay <= endDay:
        cur = conn.cursor()
        # Obtain the proper paramters for fetching one day
        startDate= currDay.strftime('%Y-%m-%d')
        nextDay = currDay + timedelta(days=1)
        nextDay = nextDay.strftime('%Y-%m-%d')

        args = [startDate, nextDay]
        rows = cur.callproc(storeProc, args)

        # Read first row
        rows = cur.fetchmany(size = 1)
        
        if len(rows) > 0: # Verify there is data
            data = np.array([rows[0]]) # Initialize data array
            rows = cur.fetchmany(size = batchSize)

            print("Iterating over data....")
            # While we have more rows, keep reading
            while len(rows) > 0:
                x = np.array(rows)
                data = np.append(data, np.array(rows),axis=0)
                rows = cur.fetchmany(size = batchSize)

            print("Saving data for days "+ startDate+ "   " +nextDay)
            output = DataFrame(data, columns = cols)
            output.to_csv(folder+startDate+'-'+fileName, index = False)
            print("Done!")
        currDay = currDay + timedelta(days=1)
            
        cur.close()

def readBoundaryLayer(conn, currDay, endDay, folder, fileName):
    print("************** Reading boundary layer *********")
    storeProc = 'lidar.get_boundary_layer_altitude'
    cols = [ 'Timestamp','ConfID','ScanID','LayerID','Azimuth','Elevation','RLA','MLA' ]
    helperIterateFunction(conn, currDay, endDay, folder, fileName, storeProc, cols)

def readRadialWindData(conn, currDay, endDay, folder, fileName):
    print("************** Reading Radial Wind *********")
    storeProc = 'lidar.get_radial_wind_data'
    cols = [ 'Timestamp','ConfID','ScanID','LOSID','Azimuth','Elevation','Range','RWS','DRWS', 'CNR' ]
    helperIterateFunction(conn, currDay, endDay, folder, fileName, storeProc, cols)


def readReconstructionWindData(conn, currDay, endDay, folder, fileName):
    print("************** Reading Reconstruction Wind *********")
    storeProc = 'lidar.get_reconstruction_wind_data'
    cols = [ 'Timestamp','ConfID','ScanID','Azimuth','Elevation','Range','Xwind','Ywind', 'Zwind' ]
    helperIterateFunction(conn, currDay, endDay, folder, fileName, storeProc, cols)
    
if __name__ == "__main__":
    # Make db connection
    conn = makeConn()

    #startDate = '2017-01-01 00:00:00'
    #endDate = '2017-09-01 00:00:00'

    batchSize = 100 
    
    try:
        folder = '/home/olmozavala/LYDAR/'
        startDay = date(2017,1,1)
        endDay =  date(2017,8,10)

        # Select dates
        # Reading RHI data
        #fileName = 'BoundaryLayer.txt'
        #readBoundaryLayer(conn, startDay, endDay, folder, fileName)

        fileName = 'ReconstWindData.txt'
        readReconstructionWindData(conn, startDay, endDay, folder, fileName)

        fileName = 'RadialWindData.txt'
        readRadialWindData(conn, startDay, endDay, folder, fileName)


    except MySQLdb.Error, e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))

    finally:
        conn.close()
