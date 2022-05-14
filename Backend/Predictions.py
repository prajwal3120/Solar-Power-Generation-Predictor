import numpy as np
import pandas as pd
import re
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import optuna
import xgboost as xgb
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import joblib

def prediction(efficiency,area):

    data2 = pd.read_csv(r"database\API_CSV.csv")

    data2['sunrise'] = data2['sunrise'].apply(lambda x: re.search(r'([01]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?', x).group(0))
    data2['sunset'] = data2['sunset'].apply(lambda x: re.search(r'([01]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?', x).group(0))

    date = data2['datetime']
    date = np.array(date)
    sunrise = data2['sunrise']
    sunrise = np.array(sunrise)
    sunset = data2['sunset']
    sunset = np.array(sunset)

    data2['Month'] = data2['datetime'].apply(lambda x: re.search(r'(?<=-)\d+(?=-)', x).group(0)).astype(int)
    data2['Day'] = data2['datetime'].apply(lambda x: re.search(r'\d+$', x).group(0)).astype(int)
    data2['Year'] = data2['datetime'].apply(lambda x: re.search(r'^\d+', x).group(0)).astype(int)

    data2 = data2.drop('datetime', axis=1)

    data2['SunriseHour'] = data2['sunrise'].apply(lambda x: re.search(r'^\d+', x).group(0)).astype(int) 
    data2['SunriseMinute'] = data2['sunrise'].apply(lambda x: re.search(r'(?<=:)\d+(?=:)', x).group(0)).astype(int)
    data2['SunriseSecond'] = data2['sunrise'].apply(lambda x: re.search(r'(\d+$)', x).group(0)).astype(int)

    data2['SunsetHour'] = data2['sunset'].apply(lambda x: re.search(r'^\d+', x).group(0)).astype(int)
    data2['SunsetMinute'] = data2['sunset'].apply(lambda x: re.search(r'(?<=:)\d+(?=:)', x).group(0)).astype(int)
    data2['SunsetSecond'] = data2['sunset'].apply(lambda x: re.search(r'(\d+$)', x).group(0)).astype(int)

    data2 = data2.drop(['sunrise','sunset'], axis=1)

    sunrise_hour = data2['SunriseHour']
    sunrise_minute = data2['SunriseMinute']/60
    sunset_hour = data2['SunsetHour']
    sunset_minute = data2['SunsetMinute']/60
    t1 = np.array(sunrise_hour) + np.array(sunrise_minute)
    t2 = np.array(sunset_hour) + np.array(sunset_minute)
    array1 = np.array(t1)
    array2 = np.array(t2)
    subtracted_array = np.subtract(t2, t1)
    daytime = subtracted_array 

    y = data2['solarradiation'].copy()
    X = data2.drop('solarradiation', axis=1).copy()

    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    dtest = xgb.DMatrix(X)

    model = joblib.load(r"database\Irradiance_XGB.pkl")
 
    a = model.predict(dtest)
    a = np.reshape(a, (15,))
    
    unit = float(efficiency * area)
    unit = np.repeat(unit,15)
    irradiance = np.array(a) 
    x = np.array(unit)
    x = x.astype(np.float)
    avg_daily_irradiance = ((irradiance * daytime)/1000)
    avg_daily_irr = np.array(avg_daily_irradiance)  
    power_gen = ((avg_daily_irr * x)/1000)
    power_generation = np.array(power_gen)
    
    avg_power_generation = np.mean(power_generation)

    temp = data2['temp']
    temp = np.array(temp)

    avg_temp = np.mean(temp)
    
    avg_daytime = np.mean(daytime)


    avg_irradiance= np.mean(irradiance)

    power_gen_units = (avg_power_generation * avg_daytime)

    avg_irradiance= np.format_float_positional(avg_irradiance, 2)
    power_gen_units = np.format_float_positional(power_gen_units, 2)
    avg_daytime = np.format_float_positional(avg_daytime, 2)
    avg_power_generation = np.format_float_positional(avg_power_generation, 2)
    avg_temp = np.format_float_positional(avg_temp, 2)

    return irradiance,daytime,power_generation,avg_power_generation, temp,avg_temp,date,sunrise,sunset,avg_daytime,avg_irradiance,power_gen_units




    