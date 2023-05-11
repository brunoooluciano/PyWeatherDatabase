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
        #add the city, state, and country information returned from the addCityOnDB funtion
        self.city = city
        self.state = state
        self.country = country
        query = f"""INSERT INTO LOCALS(CITY, STATE, COUNTRY)
        VALUES('{city}', '{state}', '{country}')"""
        self.cursor.execute(query) 
        self.cursor.commit()      

    def insertDataToCurrentWeather(self, city, temp, tempMin, tempMax, humidity, description):
        #insert data into database
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
        #extract weather database information an return a dataframe
        query = f"SELECT DATE, CITY, DESCRIPTION, HUMIDITY, TEMP, TEMP_MIN, TEMP_MAX FROM CURRENTWEATHER ORDER BY DATE DESC"
        self.cursor.execute(query)    
        results = self.cursor.fetchall()
        df = pd.DataFrame.from_records(results, 
                                        columns=[desc[0] 
                                                for desc in self.cursor.description])
        #get dataframe from selecData function and create a csv file with date format name
        now = datetime.now()
        time = now.strftime("%Y%m%d_%H%M%S")
        logDir = os.path.join("WeatherCSV")
        if not os.path.exists(logDir):
            os.makedirs(logDir)          
        fileName = f"weather_{time}_log"
        df = df.to_csv(f"WeatherCSV/{fileName}.csv", index=False)
