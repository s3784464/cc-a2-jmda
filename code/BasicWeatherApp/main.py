#!/usr/bin/env python
from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for
from weather import query_api
from weather import improve_weather_prediction
import json
import requests
from calender import Calender
app = Flask(__name__)

events = None

TO12_URL = ('https://us-central1-cc-s3784464-a2.cloudfunctions.net/to12Hour?time={}')

def to12Hour(request):
    suffix = "AM"
    
    hourAndMin = request.split(':', 1)
    hours = int(hourAndMin[0])
    if hours/12 > 1:
        hours = hours % 12
        suffix = "PM"

    return str(hours) + ':' + hourAndMin[1] + suffix


@app.route('/')
def index():
    cal = Calender()
    events = cal.buildEvents()
    weathers = []
    improve_weather_prediction(25)
    new_times = []
    for e in events:
        weathers.append(query_api(e))
        TO12_URL.format(e.getTime())
        requests.get(TO12_URL).text
        time = to12Hour(e.getTime())
        new_times.append(time)

    return render_template(
        'index.html',
        events=events,
        weathers=weathers,
        times=new_times)
@app.route("/result" , methods=['GET', 'POST'])
def result():
    data = []
    error = None
    
    select = request.form.get('comp_select')
    """ resp = query_api('Brisbane')
    pp(resp)
    if resp is not None:
       data = resp """
    if len(data) != 2:
        error = 'Bad Response from Weather API'
    return render_template(
        'result.html',
        name='TestName',
        data=weathers,
        error=error)
if __name__=='__main__':
    app.run(debug=True) 


