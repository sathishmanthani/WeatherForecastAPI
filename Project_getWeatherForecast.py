# Course Name: Introduction to Programming DSC510
# Date: 8/7/2019
# Author: Sathish Manthani
# Description: This program fetches weather forecast data using OpenWeatherMap APIs.
#               It prompts user to enter a city name or zip code and API will be called with these parameters.
#               Error message is displayed the user if connection fails or input parameters are incorrect.
#               On success, weather forecast data is displayed for next 5 days in 3 hour intervals.
# Usage: Enter a valid zip code or city name, or type exit to quit the program.


# Importing requests module which helps to connect to REST APIs
import requests, json
# Importing datetime method for date conversion
from datetime import datetime


# This method takes REST API url as input and establishes connection. Fetches response data and processes JSON data into Python dictionary and return the dictionary.
def getForecast(url):
    # Connecting to the API
    response = requests.get(url)
    # Raise exception in case of connection error and return appropriate error message.
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as exp:
        return "[Error]: Invalid Zip code or City name. Also, check your connection.\n" \
               "[Erorr]: Example input values are:   New York \n\t\t\t\t\t\t\t\t\t London,UK \n\t\t\t\t\t\t\t\t\t 10115,DE\n" \
               "[Detail Error]: " + str (exp) \
 \
    # If the connection succeeds then read the fetched JSON string
    json_resp = response.json()
    # weather_string = json.dumps(json_resp, indent=4)
    # print(weather_string)

    # Initializing list variables to store JSON data from response. Variable names are self-explonatory.
    forecast_date = []
    # temperature = []
    min_temp = []
    max_temp = []
    pressure = []
    sea_level = []
    grnd_level = []
    humidity = []
    wind_direction = []
    wind_speed = []
    description = []

    # Length of the list in the Json response to use in iteration
    response_length = len (json_resp["list"])

    # Fetch data from JSON response and append in above list variables iteratively
    for i in range(response_length):
        forecast_date.append (json_resp["list"][i]["dt"])
        # print("Time of data forecasted, unix, UTC", forecast_date)

        # temperature.append(json_resp["list"][i]["main"]["temp"])
        # print("Temperature. Unit Default: Kelvin", temperature)

        min_temp.append (json_resp["list"][i]["main"]["temp_min"])
        # print("Minimum temperature :", min_temp)

        max_temp.append (json_resp["list"][i]["main"]["temp_max"])
        # print("Maximum temperature :", max_temp)

        pressure.append (json_resp["list"][i]["main"]["pressure"])
        # print("Atmospheric pressure :", pressure)

        sea_level.append (json_resp["list"][i]["main"]["sea_level"])
        # print("Sea level",sea_level)

        grnd_level.append (json_resp["list"][i]["main"]["grnd_level"])
        # print("Ground level", grnd_level)

        humidity.append (json_resp["list"][i]["main"]["humidity"])
        # print("Humidity", humidity)

        description.append (json_resp["list"][i]["weather"][0]["description"])
        # print("Desc", description)

        wind_speed.append (json_resp["list"][i]["wind"]["speed"])
        # print("Wind Speed:", wind_speed)

        wind_direction.append (json_resp["list"][i]["wind"]["deg"])
        # print("Wind direction:", wind_direction)

    # Initialize a data dictionary to store the above variables
    data_dict = {}
    header = ["date", "min_temp", "max_temp", "pressure", "sea_level ", "grnd_level ", "humidity", "wind_direction",
              "wind_speed", "description"]
    data = [forecast_date, min_temp, max_temp, pressure, sea_level, grnd_level, humidity, wind_direction, wind_speed,
            description]

    # Assign header column name as key and list of values as Value to the dictionary
    for index, column in enumerate (header):
        data_dict[column] = data[index]

    # Add a few more elements to the dictionary
    data_dict["city_name"] = json_resp["city"]["name"]
    data_dict["latitude"] = json_resp["city"]["coord"]["lat"]
    data_dict["longitude"] = json_resp["city"]["coord"]["lon"]
    data_dict["country"] = json_resp["city"]["country"]

    # Return the final dictionary object
    return data_dict


# This method take wind direction as input and converts it into human readable compass direction.
# You can take a look at the table here - https://uni.edu/storm/Wind%20Direction%20slide.pdf
def wind_compass_dir(wind_direction):
    val = int ((wind_direction / 22.5) + .5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


# This method converts UNIX UTC time to human readable format
def timeConvert(unix_date):
    return datetime.utcfromtimestamp(unix_date).strftime('%Y-%m-%d %H:%M')


# This method converts Kelvin temperature to Farahenheit
def kelvin2farh(temp):
    kelvin = temp
    celsius = kelvin - 273
    farh = ((9 * celsius) / 5) + 32
    return round (farh)


# This method uses above functions to convert the values in the dictionary and returns the transformed data
def transform(data_dict):
    for key, value in data_dict.items ():
        if key == 'date':
            for i in range (len (value)):
                value[i] = timeConvert (value[i])
        elif key == "wind_direction":
            for i in range (len (value)):
                value[i] = wind_compass_dir (value[i])
        elif key == "max_temp" or key == "min_temp":
            for i in range (len (value)):
                value[i] = kelvin2farh (value[i])
    return data_dict


# Main function - Gets the user input and calls the above methods to transform data and prints the output
def main():
    # Welcome messages with date timestamp
    print("[{}] Welcome to Weather forecast app!".format (datetime.today ().strftime ("%Y-%m-%d %H:%M")))
    print(
        "[{}] This app provides Weather forecast for any location or city for next 5 days at 3 hours interval.".format (
            datetime.today ().strftime ("%Y-%m-%d %H:%M")))
    print(
        "[{}] Default country code is US. However, enter country code after city name or zipcode with comma to get forecast for any city outside US".format (
            datetime.today ().strftime ("%Y-%m-%d %H:%M")))
    print("[{}] Check the county codes here https://bit.ly/1MObR9o: Example input: London,UK".format (
        datetime.today ().strftime ("%Y-%m-%d %H:%M")))

    api_key = "2e692977d9ab1d495f964d3e32877d71"

    # Below While loop allows user to fetch weather data for multiple cities. Default country code is US.
    while True:
        raw_input = input ("\nEnter Zip code or City name (type 'exit' to quit):")
        # Split city/zipcode and country code
        input_list = raw_input.split (',')
        # Store city name/zipcode in processed_input
        processed_input = input_list[0]
        # If loop to check if country code is provided as second value or not. If not, US is the default country code.
        if len(input_list) == 1:
            country_code = 'us'
        else:
            country_code = input_list[1]

        # Break the loop if user enters exit
        if processed_input.lower() == 'exit' or processed_input.lower () == 'quit':
            print("Bye, Have a nice day!")
            break
        # If the input is zipcode, i.e.number then use ZIP code based REST API's URL
        elif processed_input.isnumeric ():
            zip_code = processed_input
            url = "http://api.openweathermap.org/data/2.5/forecast?zip={},{}&appid={}".format (zip_code, country_code,
                                                                                               api_key)
        # If the input is not numeric then use City Name based REST API's URL
        else:
            city_name = processed_input
            url = "https://api.openweathermap.org/data/2.5/forecast?q={},{}&appid={}".format (city_name,
                                                                                              country_code.upper (),
                                                                                              api_key)

        # Call getForecast method to get the response data into a dictionary variable.
        # Remember, getForecast() returns error message(string object) if something goes wrong
        response_data = getForecast(url)

        # Check if returned object is a dictionary and not a string. If dictionary object them proceed with transformation and output steps.
        if isinstance (response_data, dict):
            print("\n[{}] Connection established successfully to OpenWeatherMap API!".format(datetime.today().strftime ("%Y-%m-%d %H:%M")))

            # Transform the data using transform method
            transformed_data = transform(response_data)

            # Print the City name, latitude and longitude
            print("\nCity Name: {},{} \nLatitude : {}\nLongitude: {}\n".format(transformed_data['city_name'],
                                                                                 transformed_data['country'],
                                                                                 transformed_data['latitude'],
                                                                                 transformed_data['longitude']))

            # Print weather data in a readable table format
            print('|' + '-' * 20 + '|' + '-' * 20 + '|' + '-' * 8 + '-' + '-' * 8 + '|' + '-' * 11 + '|' + '-' * 13 + '|')

            # Table header rows
            print('|{:^20}|{:^20}|{:^17}|{:^11}|{:^13}|'.format ('Date Time', 'Description', 'Temperature(F)', 'Humidity',
                                                               'Wind'))
            print ('|{:^20}|{:^20}|{:^8}|{:^8}|{:^11}|{:^5}|{:^7}|'.format ('', '', 'Min', 'Max', '', 'Dir', 'Speed'))
            print (
                '|' + '-' * 20 + '|' + '-' * 20 + '|' + '-' * 8 + '|' + '-' * 8 + '|' + '-' * 11 + '|' + '-' * 13 + '|')

            # Table data rows
            for i in range(len(transformed_data['date'])):
                print('|{:^20}|{:^20}|{:7}F|{:7}F|{:10}%|{:^5}{:5}mph|'.format (transformed_data['date'][i], (
                transformed_data['description'][i]).title (), transformed_data['min_temp'][i],
                                                                                 transformed_data['max_temp'][i],
                                                                                 transformed_data['humidity'][i],
                                                                                 transformed_data['wind_direction'][i],
                                                                                 transformed_data['wind_speed'][i]))
                print('|' + '-' * 20 + '|' + '-' * 20 + '|' + '-' * 8 + '|' + '-' * 8 + '|' + '-' * 11 + '|' + '-' * 13 + '|')

        # Else, if returned object is not a dictionary then it must be error message, print it to user
        else:
            print(response_data)


# Call the main function
if __name__ == '__main__':
    main ()
