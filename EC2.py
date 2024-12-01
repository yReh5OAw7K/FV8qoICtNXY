import os
import time
import yfinance as yf
from random import gauss
from statistics import mean, stdev
import json, http.client, requests
from flask import Flask, jsonify, request
from datetime import datetime, timedelta, timezone, date

app = Flask(__name__)
static_path = app.static_folder

@app.route("/get_sig_vars9599", methods=["POST"])
def get_sig_vars9599():
    data = request.get_json()
    close = data['multiValueQueryStringParameters']['key1']
    buy = data['multiValueQueryStringParameters']['key2']
    sell = data['multiValueQueryStringParameters']['key3']
    minhistory = int(data['queryStringParameters']['key4'])
    shots = int(data['queryStringParameters']['key5'])
    t = str(data['queryStringParameters']['key6'])

    for x in range(len(close)):
         y = float(close[x])
         close[x] = y

    for x in range(len(buy)):
        y = int(buy[x])
        buy[x] = y

    for x in range(len(sell)):
        y = int(sell[x])
        sell[x] = y

    print(buy)
    list_var95 =[]
    list_var99 =[]

    if t == "Buy":
        for i in range(minhistory, len(buy)): 
            if buy[i]==1: 
                    selected_close=close[i-minhistory:i]
                    pct = [(selected_close[i] - selected_close[i-1]) / selected_close[i-1] for i in range(1,len(selected_close))]
                    mean_val = mean(pct)
                    std_val = stdev(pct)
                    simulated = [gauss(mean_val,std_val) for x in range(shots)]
                    simulated.sort(reverse=True)
                    var95 = simulated[int(len(simulated)*0.95)]
                    var99 = simulated[int(len(simulated)*0.99)]
                    list_var95.append(var95)
                    list_var99.append(var99)
                    
    elif t == "Sell":
        for i in range(minhistory, len(sell)): 
            if sell[i]==1: 
                    selected_close=close[i-minhistory:i]
                    pct = [(selected_close[i] - selected_close[i-1]) / selected_close[i-1] for i in range(1,len(selected_close))]
                    mean_val = mean(pct)
                    std_val = stdev(pct)
                    simulated = [gauss(mean_val,std_val) for x in range(shots)]
                    simulated.sort(reverse=True)
                    var95 = simulated[int(len(simulated)*0.95)]
                    var99 = simulated[int(len(simulated)*0.99)]
                    list_var95.append(var95)
                    list_var99.append(var99)
    VaR = json.dumps({
            'var95': list_var95,
            'var99': list_var99
        })          
    return jsonify(VaR)

if __name__ == '__main__':
    app.run(port = 8888, debug=True)