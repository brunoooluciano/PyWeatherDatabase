import pyodbc
import time
import os
import pandas as pd
from datetime import datetime

class Database:
    def __init__(self, driver='SQL Server',server="BRUNOPC",database="WEATHERDATA"):
        #database info
        self.driver = driver
        self.server = server
        self.database = database    
        stringConnect = f"Driver={self.driver};Server={self.server};DATABASE={self.database};"
        self.connect = pyodbc.connect(stringConnect)
        self.cursor = self.connect.cursor()
        self.cityList = []
            
    def getCityFromTableLocals(self):
        #get the cities from the table dbo.LOCALS and append them to the cityList variable
        query = "SELECT CITY FROM LOCALS"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for row in results:
            results = row[0]
            self.cityList.append(results)

    def addCityToTableLocals(self, city, state, country):
        #insert city, state, and country in dbo.LOCALS table
        self.city = city
        self.state = state
        self.country = country
        query = f"""INSERT INTO LOCALS(CITY, STATE, COUNTRY)
        VALUES('{city}', '{state}', '{country}')"""
        self.cursor.execute(query) 
        self.cursor.commit()      

    def insertDataToCurrentWeather(self, city, temp, tempMin, tempMax, humidity, description):
        #insert api response into database
        query = f"""INSERT INTO CURRENTWEATHER(DATE, CITY, TEMP, TEMP_MIN, TEMP_MAX, HUMIDITY, DESCRIPTION)
        VALUES(getdate(), '{city}', {temp}, {tempMin}, {tempMax}, {humidity}, '{description}')"""
        self.cursor.execute(query) 
        self.cursor.commit()   
    def closeConnection(self):
        #close database connection
        self.connect.close()
    
  
class Extraction(Database):
    def __init__(self, driver='SQL Server', server="BRUNOPC", database="WEATHERDATA"):
        super().__init__(driver, server, database)
    def selectDataFromCurrentWeather(self):
        #query weather database information and return a pandas dataframe
        #then create a CSV from the dataframe and write it to the WeatherCSV folder 
        #the fileName consists in the time of execution based on datetime.now() function
        query = f"SELECT DATE, CITY, DESCRIPTION, HUMIDITY, TEMP, TEMP_MIN, TEMP_MAX FROM CURRENTWEATHER ORDER BY DATE DESC"
        self.cursor.execute(query)    
        results = self.cursor.fetchall()
        df = pd.DataFrame.from_records(results, 
                                        columns=[desc[0] 
                                                for desc in self.cursor.description])
        now = datetime.now()
        time = now.strftime("%Y%m%d_%H%M%S")
        logDir = os.path.join("WeatherCSV")
        if not os.path.exists(logDir):
            os.makedirs(logDir)          
        fileName = f"weather_{time}_log"
        df = df.to_csv(f"WeatherCSV/{fileName}.csv", index=False)
