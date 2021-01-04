from flask import Flask
from flask import render_template

import requests
import json
app = Flask(__name__)


@app.route('/way/<cpn>')
def waypoints(cpn):
    cartype = cpn[0]
    province = cpn[1]
    number = cpn[2:]
    print(cartype,province,number)
    Best_path = [[18], [18, 10, 6, 11, 12], [12], [12], [9, 15, 3, 21], [
        11, 4], [4, 17], [5, 7, 20], [2, 19, 16, 14], [14, 13, 8, 1], [1]]
    return render_template('waypoints.html', province=province, number=number)

@app.route('/move')
def move():
    plist = []
    try:
        jsondata = requests.get("https://ae770067-27eb-4c02-b5cd-9620231fb68e.bspapp.com/http/get",timeout=3)
        jsondata = jsondata.replace("\'","\"")
        # print(jsondata)
        data = json.loads(jsondata)
        for point in data['data'][0]['markers']:
            plist.append([float(point['longitude']),float(point['latitude'])])
        print(plist)
    except:
        plist = [[116.478935,39.997761],[116.478939,39.997825],[116.478912,39.998549],[116.478912,39.998549],[116.478998,39.998555],[116.478998,39.998555],[116.479282,39.99856],[116.479658,39.998528],[116.480151,39.998453],[116.480784,39.998302],[116.480784,39.998302],[116.481149,39.998184],[116.481573,39.997997],[116.481863,39.997846],[116.482072,39.997718],[116.482362,39.997718],[116.483633,39.998935],[116.48367,39.998968],[116.484648,39.999861]]
    
    return render_template('move.html',plist=plist)
@app.route('/')
def index():
    return render_template('waypoints.html')
