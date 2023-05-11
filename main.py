#This code uses openweathermap api and pyodbc to generate a weather database from a list of cities.#
import os
from datetime import datetime
import time
from database import Database, Extraction
from weather import Weather

        
class Main:
    def mainRun(self):
        #instances
        db = Database()       
        export = Extraction()
        apiKey = open("apikey.txt", "r").read() 
        db.getCityFromTableLocals()
        for city in db.cityList:
            weather = Weather(city, apiKey)
            weather.getData()
            print(city)
            db.insertDataToCurrentWeather(weather.city, 
                                          weather.temp, weather.tempMin, weather.tempMax, 
                                          weather.humidity, weather.description)
        export.selectDataFromCurrentWeather()
        db.closeConnection()
main = Main()
main.mainRun()


