import requests    
class Weather:
    def __init__(self, city, apiKey):
        #OpenWeatherAPI info
        self.city = city
        self.baseURL = "https://api.openweathermap.org/data/2.5/weather?"
        self.apiKey = apiKey
        self.unit = "metric"
        self.languageCode = "pt_br"
        #URL
        self.url = self.baseURL + f"q={city}" + "&limit=1&appid=" + self.apiKey + "&units=" + self.unit + "&lang=" + self.languageCode
    def getData(self): 
        #GET method
        response = requests.get(self.url).json()
        #json key and values
        self.city = response['name']
        self.temp = response['main']['temp']
        self.tempMin = response['main']['temp_min']
        self.tempMax = response['main']['temp_max']
        self.humidity = response['main']['humidity']
        self.description = response['weather'][0]['description'].capitalize()