import sqlite3
conn = sqlite3.connect("pivotmanager.db")

c = conn.cursor()

# Create table
c.execute("CREATE TABLE sensors (idSensor TEXT PRIMARY KEY, dataType TEXT, name TEXT)")

c.execute("CREATE TABLE moisture (idMoisture INTEGER PRIMARY KEY, sensorId TEXT, depth1 REAL, depth2 REAL, depth3 REAL, depth4 REAL, vSys REAL, soilTemp REAL, dataObj TEXT, dateTime TEXT)")
c.execute("INSERT INTO moisture (sensorId, depth1, depth2, depth3, depth4, vSys, soilTemp, dataObj, dateTime) VALUES ('0', null, null, null, null, null, null, null, null)")

c.execute("CREATE TABLE weather (idWeather INTEGER PRIMARY KEY, sensorId TEXT, dataObj TEXT, dateTime TEXT)")
c.execute("INSERT INTO weather (sensorId, dataObj, dateTime) VALUES ('0', null, null, null)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()