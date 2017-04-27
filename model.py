import web
import json

db = web.database(dbn='sqlite', db='pivotmanager.db')

def storeMoistureData(strData, sampleTime):
    jsonData = json.loads(strData)    
    db.insert("moisture", sensorId=jsonData["sensorId"], depth1=jsonData["depth1"], depth2=jsonData["depth2"], depth3=jsonData["depth3"], depth4=jsonData["depth4"], vSys=jsonData["vSys"], soilTemp=jsonData["soilTemp"], dataObj=strData, dateTime=sampleTime)
    
def getMoistureUploadData():
    return db.select("dataLogs", where="uploded = 0 AND dataType='moisture'")
        
def storeWeatherData(sData):
    db.insert("dataLogs", dataType="weather", dataObj=sData)
    
def getWeatherUploadData():
    return db.select("dataLogs", where="uploded = 0 AND dataType='weather'")
    
