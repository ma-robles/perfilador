import numpy as np
from pandas import DataFrame

class DataContainer:
    """ This class is used to read files driectly from the FTP and to convert
    binary data into the proper numpy array"""

    datastr = ''
    data = []

    def readFromFTP(self,data):
        """ Reads binary data as string"""
        self.datastr+=data.decode("utf-8")

    def dataToArray(self, columns, append=False):
        """ Converts the orignal data in straing format to numpy array
            The append attribute is used to indicate that we need to append data values
        """
        tempArray = np.array(self.datastr.split('\n'))

        # Remove first and last line. First line has the header and last line
        # has wrong number of items
        temp2Array = np.array([x.split(';') for x in tempArray[1:-1]])
        #print(temp2Array[0:3])

        # Last column has empty string, remove it
        dataArray = np.array(temp2Array[:,0:-1])
        dataArray[dataArray==''] = '0'

        # Verify if we need to append previous data
        if append:
            if len(self.data) == 0:
                self.data =  DataFrame(dataArray, columns=columns)
            else:
                self.data = self.data.append(DataFrame(dataArray, columns=columns))
        else:
            self.data =  DataFrame(dataArray, columns=columns)

        # Append each column as float
        for idx in range(1,len(columns)):
            # Create a data frame with the requested columns
            self.data[columns[idx]] = self.data[columns[idx]].astype(float)

        #print('Size of data: ', self.data.shape)
        return self.data

    def fixForRHI(self):
        """ This is the change in data we need to do for RHI scans"""
        EL = self.data['Elevation']
        negIncrement= np.where(np.diff(EL) < 0)
        startIdx = negIncrement[0][0]
        self.data.loc[startIdx:,('Elevation')] = 90 + (90-EL[startIdx:])

    def clearString(self):
        self.datastr = ''
