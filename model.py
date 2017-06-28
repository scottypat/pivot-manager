import web
import json
import datetime

db = web.database(dbn='sqlite', db='pivotmanager.db')

def storeMoistureData(lstData, sampleTime):
    dbValues = []    
    
    for strMoistureData in stkMoistureData:
        jsonData = json.loads(strMoistureData)
        
        #Add date/time stamp, and copy of data string
        jsonData["dateTime"] = sampleTime
        jsonData["dataObj"] = jsonData
        
        dbValues.append(jsonData)
    
    try:
        #db.insert("moisture", sensorId=jsonData["sensorId"], depth1=jsonData["depth1"], depth2=jsonData["depth2"], depth3=jsonData["depth3"], depth4=jsonData["depth4"], vSys=jsonData["vSys"], soilTemp=jsonData["soilTemp"], dataObj=strData, dateTime=sampleTime)
        db.multiple_insert("moisture", values=dbValues)
    
    except:
        error = "Error Inserting Moisture Data: " + dbValues
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
    
