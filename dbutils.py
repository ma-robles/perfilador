import sys, string
__author__="Olmo S. Zavala Romero"

import mysql.connector
import pandas as pd
import numpy as np
import userpaths
import plotutils
from pandas import DataFrame


def getConn():
    #For Posgresql only
    try: 
        conn = mysql.connector.connect(user='download', password='d0wnl0ad', \
                                        host='10.20.9.108', database='lidar')
    except:
        print("Failed to connect to database")

    return conn

def resultToDataFrame(cur):
    data = []
    for result in cur.stored_results():
        temp = result.fetchall()
        data = temp

    # TImestamp ConfigID ScanID LOSID Azimuth Elevation Range RWS DRWS CNR
    return DataFrame(data, columns=['Timestamp','ConfiID','ScanID','LOSID','Azimuth', \
                                    'Elevation','Range','RWS','DRWS','CNR'])


if __name__ == "__main__":
    conn = getConn()

    cur = conn.cursor()
    # TODO Select the last hour or so
    # TODO Take into account the SNR in order to decide which ones to keep

    # TImestamp ConfigID ScanID LOSID Azimuth Elevation Range RWS DRWS CNR
    cur.callproc('get_radial_wind_data',args=['2017-04-26 0:00:00','2017-04-26 14:00:00'])

    # This function returns the following columns:
    data = resultToDataFrame(cur)
    data.to_csv('April26.csv')


    #print(data.shape)

#    scanIds = data['ScanID'].unique()
#    print(scanIds)
#    for scanId in scanIds:
#        EL, R, RW  = userpaths.readDataStoreProc(data, scanId)
#        # TODO Guess which scan type is and choose the plotting algorithm
#
#        # Changes the angle for those elevations that are 'after' 90 deg
#        negIncrement= np.where(np.diff(EL) < 0)
#        EL[negIncrement[0][0]:] = 90+ (90-EL[negIncrement[0][0]:])
#
#        plt = plotutils.plot_polar_scatter(RW, R, EL, "W")
#        plt.show()

    cur.close()
    conn.close()
