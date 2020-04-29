#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:24:24 2018

@author: danielatreyu
"""
import pandas
from ftplib import FTP
from pandas import DataFrame
from datetime import *
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import plotutils
import numpy as np
import os, sys, getopt
import re
#from DataContainer import *
from WindTimeSeriesHourly import windTimeSerieshourly


host = '132.248.8.31'
port = 21
inputFolder = '/perfilador/'  # Folder inside the FTP
outputFolder = '/home/perfilador/data/graficasd'
ftp = FTP() 
ftp.connect(host,port)

# This function MUST receive a date in the format 'YYYY-MM-DD' and a Time in the format 0-24
if __name__ == "__main__":

    allArguments = sys.argv[1:]
    print(allArguments)
    selectedDate = allArguments[0]
    print(selectedDate)
    hour = int(allArguments[1])
    print(hour)
    times = ['%.2d-00' % hour]
    print(times)

    # Login into the FTP server
    print(ftp.login())     
    
    windTimeSerieshourly(ftp, inputFolder, selectedDate, times[0], outputFolder, 2500)
    
    ftp.quit()
