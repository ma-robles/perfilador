import sys, string
__author__ = "Olmo S. Zavala Romero"

import numpy as np

def getDataFolder():
    """ This function should return the folder path to the data is stored"""
    # This is the part that should change in every computer (and not added into the repository)
    return "/home/olmozavala/Dropbox/MyProjects/LidarVisualization/Visualization_Python/testData/"

def getFileNamePPI():
    return 'WLS100s-90_radial_wind_data_2017-01-26_01-03-09_19_PPI_32.csv'

def getFileNameRHI():
    return 'WLS100s-90_radial_wind_data_2017-01-26_01-19-21_19_RHI_30.csv'

def getFileNameVertical():
    return 'WLS100s-90_wind_reconstruction_data_2017-01-26_04-32-43_19_DBS_33.csv'

def getFileBoundary():
    return 'WLS100s-90_boundary_layer_altitude_2017-02-25_09-20-05_7_FIXEDFORPBL_12'

def readDataFromCSV(fileName, fileType):
    csv = np.genfromtxt (fileName, delimiter=";")
    timestamp=csv[1:,0]
    LOS=csv[1:,3]
    AZ=csv[1:,4] # Azimuth
    EL=csv[1:,5] # Elevation
    R =csv[1:,6] # Range
    RW =csv[1:,7] # Radial Wind Speed

    return [timestamp, LOS, AZ, EL, R, RW]

def readDataStoreProc(data, scanId):
    rows =  data['ScanID'] == scanId
    currScan = data[rows]

    EL = currScan['Elevation'].as_matrix()
    RW = currScan['RWS'].as_matrix()
    R = currScan['Range'].as_matrix()

    return [EL, R, RW]
