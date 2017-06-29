import web
import json
import datetime

db = web.database(dbn='sqlite', db='pivotmanager.db')

def storeMoistureData(lstData, sampleTime):
    dbValues = []    
    
    for strMoistureData in lstData:
        jsonData = json.loads(strMoistureData)
        
        #Add date/time stamp, and copy of data string
        jsonData["dateTime"] = sampleTime
        sData = str(jsonData)
        jsonData["dataObj"] = sData
        jsonData.pop("loggerId", None)
        
        dbValues.append(jsonData)
    
    try:        
        db.multiple_insert("moisture", values=dbValues)
    
    except:
        error = "Error Inserting Moisture Data"
        print error
    
def getMoistureUploadData():
    return db.select("dataLogs", where="uploded = 0 AND dataType='moisture'")

def getMoistureLabels(weekDelta):
    queryDate = datetime.datetime.now() - datetime.timedelta(weeks=weekDelta)
    queryDate = queryDate.strftime('%Y/%m/%d %H:%M:%S')    
    #return db.select("moisture", what='dateTime', order='dateTime')
    return db.select("moisture", queryDate, what='dateTime', order='dateTime', where='dateTime > 2017/04/05 01:12:35')    
        
def storeWeatherData(sData):
    db.insert("dataLogs", dataType="weather", dataObj=sData)
    
def getWeatherUploadData():
    return db.select("dataLogs", where="uploded = 0 AND dataType='weather'")
    
