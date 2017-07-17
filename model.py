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

def getMoistureData(weekDelta):
    queryDate = datetime.datetime.now() - datetime.timedelta(weeks=weekDelta)
    queryDate = queryDate.strftime('%Y/%m/%d %H:%M:%S')   
    queryDate = dict(qDate=queryDate)    
    return db.query("SELECT sensorId, depth1, depth2, depth3, depth4, soilTemp, dateTime FROM moisture WHERE dateTime > $qDate", queryDate)   
        
def storeWeatherData(sData):
    db.insert("dataLogs", dataType="weather", dataObj=sData)
    
def getWeatherUploadData():
    return db.select("dataLogs", where="uploded = 0 AND dataType='weather'")
    
def orgMoistureData(moistureData):
    chartData = {}
    chartData["depth1"] = []
    chartData["depth2"] = []
    chartData["depth3"] = []
    chartData["depth4"] = []
    for dataSample in moistureData:
        singleSample = dict(dataSample)       
        chartData["depth1"].append("{x: \"" + singleSample["dateTime"] + "\", y: " +  str(singleSample["depth1"]) + "}")        
        chartData["depth2"].append("{x: \"" + singleSample["dateTime"] + "\", y: " +  str(singleSample["depth2"]) + "}")
        chartData["depth3"].append("{x: \"" + singleSample["dateTime"] + "\", y: " +  str(singleSample["depth3"]) + "}")
        chartData["depth4"].append("{x: \"" + singleSample["dateTime"] + "\", y: " +  str(singleSample["depth4"]) + "}")
    
    return chartData
        