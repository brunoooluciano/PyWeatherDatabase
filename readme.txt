This code demonstrates the use of classes, database connection, and inheritance.
The "Weather" class consumes OpenWeather's Current Weather Data API.
The "Database" class is responsible for connecting to the database and executing queries.
The "Extraction" is a child class from "Database" and is responsible for the process of exporting the data to a CSV file, 
using the Pandas library.
And  "Main" class is responsible for instantiating the other classes, open the API key file, for loop over each city from dbo.LOCALS and manage the functions.
