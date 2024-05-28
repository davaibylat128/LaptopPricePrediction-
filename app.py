from flask import Flask, render_template, request, jsonify
from bokeh.embed import server_session
from bokeh.client import pull_session
from index import js, div, cdn_jss
import pickle 
import numpy as np
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

cols = ['Company', 'TypeName', 'Ram', 'Weight', 'TouchScreen', 'Ips', 'ppi',
       'Cpu_Brand', 'Hdd', 'Ssd', 'Hybrid', 'Flash_Storage', 'Gpu_Brand', 'os']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", js=js, div=div, cdn_jss = cdn_jss)

# x_samp = pd.DataFrame([['HP', 'Ultrabook', 4, 1.3, 0, 1, 222.3,'Intel Core i3', 0, 128, 0, 0, 'Intel', 'Windows' ]], columns=cols)

# result = model.predict(x_samp)
# print(result)

@app.route("/predict", methods=['POST'])
def prediction():
    if request.method == 'POST':
        Company = request.form['company']
        TypeName = request.form['typename']
        Ram = request.form['ram']
        Weight = float(request.form['weight'])
        TouchScreen = request.form['touchscreen']
        Ips = request.form['ips']
        ppi = float(request.form['ppi'])
        Cpu_Brand = request.form['cpuname']
        Hdd = request.form['hdd']
        Ssd= request.form['ssd']
        Hybrid = request.form['hybrid']
        Flash_Storage = request.form['flash']
        Gpu_Brand = request.form['gpuname']
        os = request.form['opsys']

        sample = [[Company, TypeName, Ram, Weight, TouchScreen, Ips, ppi,
       Cpu_Brand, Hdd, Ssd, Hybrid, Flash_Storage, Gpu_Brand, os]]
        x=pd.DataFrame(sample, columns=cols)
        result = model.predict(x)
        print(result)
        return render_template("output.html", value=result)


if __name__=="__main__":
    app.run(debug=True)