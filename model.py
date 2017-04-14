import web

db = web.database(dbn='sqlite', host='localhost', db='farming')

def storeMoistureData(stkData, sampleTime):
    db.insert("datalogs", dataType="moisture", dataObj=stkData, sampleTime=sampleTime)
    
def getMoistureUploadData():
    return db.select("datalogs", where="uploded = 0 AND dataType='moisture'")
        
def storeWeatherData(sData):
    db.insert("datalogs", dataType="weather", dataObj=sData)
    
def getWeatherUploadData():
    return db.select("datalogs", where="uploded = 0 AND dataType='weather'")
    
