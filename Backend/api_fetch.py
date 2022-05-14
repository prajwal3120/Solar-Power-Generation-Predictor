import numpy as np
import pandas as pd
import csv 
import json
import requests

def api_fetch(location):

    loc = location
    key = "YNKKMA3A5N6QQW6FFKDRMZ8KL"
    response = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/location="+loc+"?unitGroup=metric&key="+key+"&include=days&elements=datetime,tempmax,tempmin,temp,feelslikemax,feelslikemin,feelslike,dew,humidity,windgust,windspeed,winddir,sealevelpressure,cloudcover,visibility,solarradiation,solarenergy,uvindex,sunrise,sunset,moonphase").json()
    location = response['resolvedAddress']

    with open(r"database\api_data.json", 'w') as json_file:
        json.dump(response, json_file)

    with open(r"database\api_data.json") as json_file:
        data = json.load(json_file)
 
    datetime_data = data['days']
 
    # now we will open a file for writing
    data_file = open(r"database\API_CSV.csv", 'w')
 
    # create the csv writer object
    csv_writer = csv.writer(data_file)
 
    # Counter variable used for writing
    # headers to the CSV file
    count = 0
 
    for days in datetime_data:
        if count == 0:
 
            # Writing headers of CSV file
            header = days.keys()
            csv_writer.writerow(header)
            count += 1
 
        # Writing data of CSV file
        csv_writer.writerow(days.values())
 
    data_file.close()
    return location