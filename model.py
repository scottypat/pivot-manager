import web

db = web.database(dbn='sqlite', host='localhost', db='pivotmanager')

def storeMoistureData(stkData, sampleTime):
    db.insert("dataLogs", dataType="moisture", dataObj=stkData, dateTime=sampleTime)
    
def getMoistureUploadData():
    return db.select("dataLogs", where="uploded = 0 AND dataType='moisture'")
        
def storeWeatherData(sData):
    db.insert("dataLogs", dataType="weather", dataObj=sData)
    
def getWeatherUploadData():
    return db.select("dataLogs", where="uploded = 0 AND dataType='weather'")
    
