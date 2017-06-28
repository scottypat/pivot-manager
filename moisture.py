import wiringpi
import httplib
import json
import string
import sys

def setupLora():
    wiringpi.wiringPiSetup()
    loraId = wiringpi.serialOpen("/dev/serial0",9600)
    wiringpi.pinMode(4, 1) # P1 Pin
    wiringpi.pinMode(5, 1) # P2 Pin
    wiringpi.digitalWrite(4, 1) 
    wiringpi.digitalWrite(5, 0)
    return  loraId

def getData(loraId, loggerId):
    lstMoistureData = []
    bMoistureData = False
    
    while wiringpi.serialDataAvail(loraId) > 0:
        intDataChar = wiringpi.serialGetchar(loraId)
        strDataChar = chr(intDataChar)
        
        if strDataChar == "$":
            bMoistureData = True
            strMoistureData = ""
        
        if bMoistureData == True:
            strMoistureData =  strMoistureData + strDataChar
        
        if strDataChar == "!" and bMoistureData == True:
            # Trim start and end characters, and load json data
            strMoistureData = strMoistureData[2:-2]
            try:
                jsonData = buildJson(strMoistureData)                
                #Check if data is intended for this data logger            
                if jsonData["loggerId"] == loggerId:   
                    lstMoistureData.append(strMoistureData)           
                
            except ValueError, e:
                print "Unable to load weather data: " + strMoistureData 
            
            bMoistureData = False                
            strMoistureData = ""     
           
    return lstMoistureData

def postData(lstMoistureData, farmingServer):
    headers = ""
    conn = httplib.HTTPConnection(farmingServer)
    conn.request("POST", "/moisture", lstMoistureData, headers)
    response = conn.getresponse()
    
    if response.status == "200":
            content = response.read()        
            data = json.loads(content)
            return data
        
def buildJson(strMoistureData):
    arrayPosition = 0
    dbStructure = {}
    dataStructure = {
        0: 'sensorId',
        1: 'loggerId',
        2: 'depth1',
        3: 'depth2',
        4: 'depth3',
        5: 'depth4',
        6: 'vSys',
        7: 'soilTemp'}    
    
    splitMoistureData = strMoistureData.split(",")
    
    jsonWeatherData = "{"
    
    for moistureData in splitMoistureData:
        if arrayPosition in dataStructure.keys():
            jsonWeatherData = jsonWeatherData + "\"" + dataStructure[arrayPosition] + "\""
            jsonWeatherData = jsonWeatherData + ":"
            if dataStructure[arrayPosition] == "sensoId" or dataStructure[arrayPosition] == "loggerId":
                jsonWeatherData = jsonWeatherData + "\"" + moistureData + "\""
            else:
                jsonWeatherData = jsonWeatherData + moistureData
            jsonWeatherData = jsonWeatherData + "," 
                       
        array_position += 1
    
    #Remove final comma     
    jsonWeatherData = jsonWeatherData[0:-1]
    
    jsonWeatherData = jsonWeatherData + "}"
    
    return jsonWeatherData
    
    
    
    
    
        