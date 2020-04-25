

import sys, string
__author__="Olmo S. Zavala Romero"

#for Posgresql only
import psycopg2

def readFile(fileName):
    "Reads and prints all the lines in a file"
    #The with statment is used as a try, catch finally
    text = ''
    with open(fileName) as file:
        #If you want to iterate manually use file.readline()
        for line in file:
            text += line

    return text

def writeToFile(fileName, data, mode):
    """ Writes 'data' to a file name. mode it can be 'a' or 'w' to appendo or write """
    f = open(fileName,mode)
    if mode == "a":
        f.write('\n')
    f.write(data)

def filesInDir(dirPath):
    dirList = os.listdir(dirPath)
    return dirList

def nameFromPath(filePath):
    """Obtains the file name from a path"""
    indx = filePath.rindex('/')
    name = filePath[indx+1:len(filePath)]
    return name

def rmExt(fileName):
    """Removes the extension of a file name"""
    indx = fileName.rindex('.')
    name = fileName[0:indx]
    return name

def postgresqlExamle():
    #For Posgresql only
    try: 
        conn = psycopg2.connect("dbname='DeepCDev' user='DeepC-DevUser' host='web-04.coaps.fsu.edu' password='devenvision@DEEPC'")
    except:
        print("Failed to connect to database")

    cur = conn.cursor();
    cur.execute("""SELECT * FROM all_cruises""");
    rows = cur.fetchall();

    print("Here comes the table:\n")
    for row in rows:
        print("   ",row[0]," - ", row[1])


if __name__ == "__main__":
    print("Yeah babe\n")
    postgresqlExamle();

