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
        if singleSample["depth1"] > 0:
            chartData["depth1"].append("{x: \"" + singleSample["dateTime"] + "\", y: " +  str(kpaMoistureData(singleSample["depth1"])) + "}")        
        
        if singleSample["depth2"] > 0:
            chartData["depth2"].append("{x: \"" + singleSample["dateTime"] + "\", y: " +  str(kpaMoistureData(singleSample["depth2"])) + "}")
        
        if singleSample["depth3"] > 0:
            chartData["depth3"].append("{x: \"" + singleSample["dateTime"] + "\", y: " +  str(kpaMoistureData(singleSample["depth3"])) + "}")
        
        if singleSample["depth4"] > 0:
            chartData["depth4"].append("{x: \"" + singleSample["dateTime"] + "\", y: " +  str(kpaMoistureData(singleSample["depth4"])) + "}")
    
    return chartData  
    

def kpaMoistureData(ohmReading):
    ohmReading = ohmReading / 1000
    soilTemp = 24
    if ohmReading > 1:        
        return (-3.213 * ohmReading - 4.093) / (1 - 0.009733 * ohmReading - 0.01205 * soilTemp)
    
    elif ohmReading > 8:
         return -2.246 - 5.239 * ohmReading * (1 + 0.015 * (soilTemp -24)) - 0.06756 * ohmReading^2 * (1 + 0.018 * (soilTemp - 24))^2
            
    else:
        return -20 * (ohmReading * (1 + 0.018 * (soilTemp - 24)) - 0.55)        