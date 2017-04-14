import logging
import argparse
import sys
import time
import model
import weather
import moisture

# Defaults
LOG_FILENAME = "/var/log/farming/pivotpoint.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
        LOG_FILENAME = args.log

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

#Collection Rate in Minutes
iMoistureCollectionRate = 60
iWeatherCollectionRate = 10
iLoopCounter = 0

#Setup LORA Radio
loraId = moisture.setupLora()

# Loop forever
while True:
        #logger.info("The counter is now ")
        
        #Get, Store Weather Data                        
        sWeatherData = weather.getData("192.168.1.141", "/FullDataString")
        model.storeWeatherData(sWeatherData)   
                      
        #Get, Store Moisture Data
        stkMoistureData = moisture.getData(loraId)        
        for strMoistureData in stkMoistureData:
            model.storeMoistureData(strMoistureData)        
        
        #Upload Weather Data to FarmingApp
        oWeatherData = model.getWeatherUploadData()
        weather.postData(oWeatherData, "farming")
        
        #Upload Moisture Data to FarmingApp
        oMoistureData = model.getMoistureUploadData()
        moisture.postData(oMoistureData, "farming")
        
        iLoopCounter += iLoopCounter        
        time.sleep(600)
        