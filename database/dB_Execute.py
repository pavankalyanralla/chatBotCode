
from database.dB_Connect import mysql
from datetime import datetime, timedelta


def fetchAll(query,tableName):
    dBcursor = mysql.get_db().cursor()
    dBcursor.execute(query+''+tableName)
    response=dBcursor.fetchall()
    dBcursor.close()
    return response

def fetchOne(query,tableName):
    dBcursor = mysql.get_db().cursor()
    dBcursor.execute(query+''+tableName)
    response=dBcursor.fetchone()
    dBcursor.close()
    return response

def fetchAllWhere(query,*argV):
    dBcursor = mysql.get_db().cursor()
    dBcursor.execute(query,argV)
    response=dBcursor.fetchall()
    dBcursor.close()
    return response

def fetchOneWhere(query,*argV):
    dBcursor = mysql.get_db().cursor()
    dBcursor.execute(query,argV)
    response=dBcursor.fetchone()
    dBcursor.close()
    return response

def InsertIntoDB(query,*argV):
    dBcursor = mysql.get_db().cursor()
    response=dBcursor.execute(query,argV)
    mysql.get_db().commit()
    dBcursor.close()
    return response    

def UpdateInDB(query,*argV):
    dBcursor = mysql.get_db().cursor()
    response=dBcursor.execute(query,argV)
    mysql.get_db().commit()
    dBcursor.close()
    return response    

def DeleteInDB(query,*argV):
    dBcursor = mysql.get_db().cursor()
    response=dBcursor.execute(query,argV)
    mysql.get_db().commit()
    dBcursor.close()
    return response

def callStoredProc(name,*argV):
    dBcursor = mysql.get_db().cursor()
    dBcursor.callproc(name,argV)
    response=dBcursor.fetchall()
    dBcursor.close()
    return response

