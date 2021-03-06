#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:44:05 2018

@author: danielatreyu
"""


# Hora UTC?
# Agregar la curva de la altura de la capa límite
# Eje vertical en milibares?


from datetime import datetime
from dateutil import tz
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import plotutils
import numpy as np
import pandas as pd
import os
import re
from DataContainer import *

def mkdirp(path):
    os.makedirs(path, exist_ok=True)
    
    
def windTimeSeries(ftp, rootFolder, selectedDate, outputFolder, ymax):
    
    """ This function uses daily DBS wind reconstruction data from the WindCube Profiler
    files, to plot a Time Series of the the horizontal and vertical components 
    of the wind """
    
    dataType = 'wind_reconstruction_data'
    file_list = []
    

    # Retrieve data from folders in FTP
    
    possible_hours = [format(x,'02d') for x in range(24)]
    from_zone = tz.gettz('America/Mexico_City')
    to_zone = tz.gettz('UTC')
    
    for item in possible_hours:
              
        local_time = datetime.strptime(selectedDate+item, '%Y-%m-%d%H')
        local_time = local_time.replace(tzinfo=from_zone)
        
        utc_date = local_time.astimezone(to_zone)
        
        utc_day = utc_date.strftime("%Y-%m-%d")
        
        utc_hour = utc_date.strftime("%H")
            
        time_folder = rootFolder+utc_day+'/'+dataType+'/'+utc_hour+'-00/'
           
        creat_min = []
        try:

            ftp.dir(time_folder, creat_min.append)
            dbs = []
            for i in range(len(creat_min)):
                if creat_min[i].find('DBS') != -1:
                    dbs.append(creat_min[i])

            if len(dbs) == 0:
                file_list.append('missing_data_'+utc_day+'_'+utc_hour+'-25')
                file_list.append('missing_data_'+utc_day+'_'+utc_hour+'-55')

            elif len(dbs) == 1:
                if dbs[0].find('-25-'):
                    file_list.append(time_folder+dbs[0][55:])
                    file_list.append('missing_data_'+utc_day+'_'+utc_hour+'-55')
                elif dbs[0].find('-55-'):
                    file_list.append('missing_data_'+utc_day+'_'+utc_hour+'-25')
                    file_list.append(time_folder+dbs[0][55:])
            else:
                for i in range(len(dbs)):
                    file_list.append(time_folder+dbs[i][55:])

        except:
            file_list.append('missing_data_'+utc_day+'_'+utc_hour+'-25')
            file_list.append('missing_data_'+utc_day+'_'+utc_hour+'-55')


         
    # Create output folder
    outputFolder = outputFolder+'/'+selectedDate
    try:
        mkdirp(outputFolder)
    except:
        print('warning: folder '+outputFolder+' already exists')
        
    # Make 'generic' outputfile
    outFile = outputFolder+'/'

    try:
        
        meas_time = []
        Usets = []
        Vsets = []
        Wsets = []
        
        for working_file in file_list:

            if working_file.find('missing_data') != -1:
                Xset = pd.DataFrame(np.nan,columns=['Xwind'],index=range(100,2550,50))
                Yset = pd.DataFrame(np.nan,columns=['Ywind'],index=range(100,2550,50))
                Zset = pd.DataFrame(np.nan,columns=['Zwind'],index=range(100,2550,50))
                match = (re.search('\d{4}-\d{2}-\d{2}_\d{2}-\d{2}',working_file)).group(0)
                meas_time.append(match)

            else:    
                match = (re.search('\d{4}-\d{2}-\d{2}_\d{2}-\d{2}',working_file)).group(0)
                #hour_min = re.search('_\d{2}-\d{2}-\d{2}',working_file).group(0)
                meas_time.append(match)
            
                obj = DataContainer()
                ftp.retrbinary('RETR %s' % working_file, obj.readFromFTP)
                columns = ['Timestamp', 'Azimuth', 'Elevation','Range','Xwind','Ywind','Zwind',\
                                'CNR','ConfIdx']

                # Get the date from the file as a DataFrame
                data = obj.dataToArray(columns)
                data.drop(data[data.Range > ymax].index, inplace=True)
                data = data[['Range','Xwind','Ywind','Zwind']]
                # Replace abs values Xwind and Ywind greater than 50 with NaN
                
                data.Xwind.where((data.Xwind < 50) | (data.Xwind > -50),np.nan,inplace=True)
                data.Ywind.where((data.Ywind > 50) | (data.Ywind > -50),np.nan,inplace=True)

                dataByRange = data.groupby('Range').mean()          
            
                Xset = dataByRange[['Xwind']]
                Yset = dataByRange[['Ywind']]
                Zset = dataByRange[['Zwind']]
            
            Usets.append(Xset)
            Vsets.append(Yset)
            Wsets.append(Zset)
                         
        df_U = pd.concat(Usets,axis=1)
        df_V = pd.concat(Vsets,axis=1)
        df_W = pd.concat(Wsets,axis=1)
        
        U = df_U.values;
        V = df_V.values;
        W = df_W.values;
        
        # Vertical wind grid
        x = np.linspace(0,48,49)
        y = np.linspace(100,2500,49)
        X, Y = np.meshgrid(x, y)
        
        # If the plot is going to have a variable pcolormesh uncomment next section
#        cmapLim = 0
#        if abs(np.nanmax(W)) > abs(np.nanmin(W)):
#            cmapLim = abs(np.nanmax(W))
#        else:
#            cmapLim = abs(np.nanmin(W))
            
        # Change back the UTC times to local time
        
        timelabels = []
        to_zone = tz.gettz('America/Mexico_City')
        from_zone = tz.gettz('UTC')
        
        for entry in meas_time:
            utc_time = datetime.strptime(entry, '%Y-%m-%d_%H-%M')
            utc_time = utc_time.replace(tzinfo=from_zone)
        
            local = utc_time.astimezone(to_zone)
        
            timelabels.append(local.strftime("%H:%M"))
        
        timelabels = [i.replace('25','00') for i in timelabels[2:48:4]]
        
        # Plot 
        title = ('Perfil vertical del viento, %s (serie de tiempo)' % selectedDate)
        fig, ax = plt.subplots(figsize=(20,8))
        
        # For variable pcolormesh uncomment next line
        #cax = ax.pcolormesh(X, Y, W, cmap='seismic', vmin= (-cmapLim), vmax=cmapLim)
        
        cax = ax.pcolormesh(X, Y, W, cmap='seismic', vmin= -3, vmax=3)
        ax.set_title(title,fontsize = 24)
        ax.set_xlabel('Hora Local [hh:mm]', fontsize = 18, labelpad = 14)
        ax.set_xticks(np.arange(2.5,48, step=4))
        ax.set_xticklabels(timelabels, rotation=45, size=12)
        ax.set_ylabel('Altura [m]', fontsize = 18, labelpad = 18)
        ax.yaxis.set_tick_params(labelsize=12)
        ax.text(0.18,-0.08,'Datos de perfilador LIDAR Leosphere Windcube 100s. Lat 19.3262, Lon -99.1761, Alt 2280 msnm',transform=plt.gcf().transFigure, fontdict={'size': 18})
        
        # Colorbar
        cbaxes = fig.add_axes([0.91, 0.125, 0.02, 0.4]) 
        cbar = fig.colorbar(cax, cax = cbaxes)
        cbar.set_label(r'Viento vertical [$m\,s^{-1}$]', fontsize = 18)
        cbaxes.text(-0.3,1.07,'(Hacia arriba)')
        cbaxes.text(-0.3,-0.07,'(Hacia abajo)') 
        
        
        #Other a artists
        im = mpimg.imread('/home/perfilador/perfila/drozanes/resources/time_adv.png')
        newax = fig.add_axes([0.6, -.03, 0.06, 0.06], anchor='NW', zorder=0) #[xo,yo,width,height]
        newax.imshow(im)
        newax.axis('off')
        
        im = mpimg.imread('/home/perfilador/perfila/drozanes/resources/directions.png')
        newax1 = fig.add_axes([0.90, 0.75, 0.15, 0.15], anchor='NW', zorder=0) #[xo,yo,width,height]
        newax1.imshow(im)
        newax1.axis('off')
        
        
        # Horizontal wind grid
        
        x_h = np.arange(0, len(meas_time), 1)
        Xh, Yh = np.meshgrid(x_h, y)
        
        # Plot arrows
        Q = ax.quiver(Xh[::2], Yh[::2], U[::2], V[::2], pivot = 'mid',alpha=0.75)
        ax.quiverkey(Q, 0.93, 0.68, 10, r'$10\,m\,s^{-1}$',coordinates = 'figure', labelpos='N' )
        
        
        finalOutputFile = outFile+'timeseries_daily_'+selectedDate
        fig.savefig(finalOutputFile,bbox_inches='tight')
        plt.close()
        
    except Exception as e:
        print("Problema calculando Wind Time Series", e)
