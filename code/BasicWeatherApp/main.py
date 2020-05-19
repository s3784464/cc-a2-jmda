#!/usr/bin/env python
from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for
from weather import query_api
import json
app = Flask(__name__)
@app.route('/')
def index():
    return render_template(
        'weather.html',
        data=[{'name':'Melbourne','coord':'lat=37.8136&lon=144.9631'}, {'name':'Montreal'}, {'name':'Calgary'},
        {'name':'Ottawa'}, {'name':'Edmonton'}, {'name':'Mississauga'},
        {'name':'Winnipeg'}, {'name':'Vancouver'}, {'name':'Brampton'}, 
        {'name':'Quebec'}])
@app.route("/result" , methods=['GET', 'POST'])
def result():
    data = []
    error = None
    select = request.form.get('comp_select')
    resp = query_api('Brisbane')
    pp(resp)
    if resp is not None:
       data = resp
    if len(data) != 2:
        error = 'Bad Response from Weather API'
    return render_template(
        'result.html',
        name='TestName',
        fc=data,
        error=error)
if __name__=='__main__':
    app.run(debug=True) 