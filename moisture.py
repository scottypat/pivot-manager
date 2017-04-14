import wiringpi
import httplib
import json

strMoistureData = ""
stackMoistureData = []

def setupLora():
    wiringpi.wiringPiSetup()
    loraId = wiringpi.serialOpen("/dev/serial0",9600)
    return  loraId

def getData(loraId):
    while wiringpi.serialDataAvail(loraId) > 0:
        intDataChar = wiringpi.serialGetchar(loraId)
        strDataChar = chr(intDataChar)
        
        if strDataChar == "$":
            bMoistureData = True
        
        if bMoistureData == True:
            strMoistureData += strDataChar
        
        if strDataChar == "!":
            bMoistureData = False
            stackMoistureData.append(strMoistureData)
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