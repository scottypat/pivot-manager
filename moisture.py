import wiringpi
import httplib
import json
import string
import sys

def setupLora():
    wiringpi.wiringPiSetup()
    loraId = wiringpi.serialOpen("/dev/serial0",9600)
    return  loraId

def getData(loraId, loggerId):
    stackMoistureData = []
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
                jsonData = json.loads(strMoistureData)
            
                #Check if data is intended for this data logger            
                if jsonData["loggerId"] == loggerId:   
                    stackMoistureData.append(strMoistureData)
            except ValueError, e:
                print "Unable to load jsonData: " + strMoistureData
                print e
                
            bMoistureData = False                
            strMoistureData = ""
     
    bMoistureData = False                
    strMoistureData = ""       
    return stackMoistureData

def postData(stackMoistureData, farmingServer):
    headers = ""
    conn = httplib.HTTPConnection(farmingServer)
    conn.request("POST", "/moisture", stackMoistureData, headers)
    response = conn.getresponse()
    
    if response.status == "200":
            content = response.read()        
            data = json.loads(content)
            return data