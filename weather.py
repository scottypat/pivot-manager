import json
import httplib

# set up your OurWeather IP Address here
uri = '192.168.1.141'
path = '/FullDataString'

# fetch the JSON data from the OurWeather device
def getData(uri, path):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8'
        }
    body = ""
    conn = httplib.HTTPConnection(uri)
    conn.request("GET", path, body, headers)
    response = conn.getresponse()
    
    if response.status == "200":
        content = response.read()        
        data = json.loads(content)
        return data

def postData(jsonData, farmingServer):
    headers = {'Content-Type': 'application/json'}
    conn = httplib.HTTPConnection(farmingServer)
    conn.request("POST", "/weather", jsonData, headers)
    response = conn.getresponse()
    
    if response.status == "200":
            content = response.read()        
            data = json.loads(content)
            return data