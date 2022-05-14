from distutils.log import info
from flask import Flask,request, jsonify, url_for, redirect, render_template
import pickle
import numpy as np
from sklearn.metrics import r2_score
from Backend.api_fetch import api_fetch
from Backend.Predictions import prediction
import json

app = Flask(__name__, template_folder = 'Frontend', static_folder = 'Frontend')

model=pickle.load(open('database\irradiance_XGB.pkl','rb'))


@app.route('/')
def homepage():
    return render_template('Homepage.html')


@app.route('/predict',methods=['POST','GET'])
def predict():
    location = request.form['city']
    efficiency = int(request.form['efficiency'])
    area = int(request.form['area'])
    location = api_fetch(location)

    irradiance = prediction(efficiency,area)[0]
    daytime = prediction(efficiency,area)[1]
    power_generation = prediction(efficiency,area)[2]
    avg_power_generation = prediction(efficiency,area)[3]
    temp = prediction(efficiency,area)[4]
    avg_temp = prediction(efficiency,area)[5]
    date = prediction(efficiency,area)[6]
    sunrise = prediction(efficiency,area)[7]
    sunset = prediction(efficiency,area)[8]
    avg_daytime = prediction(efficiency,area)[9]
    avg_irradiance = prediction(efficiency,area)[10]
    power_gen_units = prediction(efficiency,area)[11]
    r2_score = 0.98


    return render_template('Dashboard.html',date=date,irradiance=irradiance,daytime=daytime,power_generation=power_generation,avg_power_generation=avg_power_generation,temp=temp,avg_temp=avg_temp,sunrise=sunrise,sunset=sunset,location=location,efficiency=efficiency,area=area,r2_score=r2_score,avg_daytime=avg_daytime,avg_irradiance=avg_irradiance,power_gen_units=power_gen_units)

if __name__ == '__main__':
    app.run(debug=True)
