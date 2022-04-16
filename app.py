from distutils.log import info
from flask import Flask,request, jsonify, url_for, redirect, render_template
import pickle
import numpy as np
from sklearn.metrics import r2_score
from api_fetch import api_fetch
from Predictions import prediction
import json

app = Flask(__name__)

model=pickle.load(open('database\irradiance_XGB.pkl','rb'))


@app.route('/')
def hello_world():
    return render_template("home.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    location = request.form['city']
    wattage = request.form['Panel_Wattage']
    api_fetch(location)

    irradiance = prediction(wattage)[0]
    daytime = prediction(wattage)[1]
    power_generation = prediction(wattage)[2]
    avg_power_generation = prediction(wattage)[3]
    temp = prediction(wattage)[4]
    avg_temp = prediction(wattage)[5]
    date = prediction(wattage)[6]
    sunrise = prediction(wattage)[7]
    sunset = prediction(wattage)[8]
    r2_score = 0.9807567558305414

    irradiance = irradiance.tolist()
    date = date.tolist()
    # class NumpyEncoder(json.JSONEncoder):
    #     def default(self, obj):
    #         if isinstance(obj, np.ndarray):
    #             return obj.tolist()
    #         return json.JSONEncoder.default(self, obj)
    # json_data = json.dumps({'irradiance': irradiance, 'daytime': daytime, 'power_generation': power_generation, 'avg_power_generation':avg_power_generation,'temp':temp,'avg_temp':avg_temp,'date':date,'sunrise':sunrise,'sunset':sunset,'location':location,'wattage':wattage,'r2_score':r2_score}, 
    #                    cls=NumpyEncoder)

    data = [irradiance,daytime,power_generation,avg_power_generation, temp,avg_temp,date,sunrise,sunset,location,wattage,r2_score]

    return render_template('dashboard.html' , irradiance = irradiance, date=date)

if __name__ == '__main__':
    app.run(debug=True)
