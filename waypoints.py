from flask import Flask
from flask import render_template

import requests
import json
app = Flask(__name__)
    
# waylist = [[116.583727,39.766743],[116.722967,40.047705],[116.606476,39.842024],[116.57941,39.91557],[116.471384,39.871168],[116.277783,39.950124],[116.167924,39.81632],[116.345488,39.796036],[116.460962,39.819879],[116.186757,39.745945],[116.590903,40.14285],[116.597232,40.204182],[116.528726,40.011064],[116.453963,39.953477],[116.264293,40.122599],[116.397414,39.988556],[116.475507,39.998146],[116.614531,40.112563],[116.681114,39.709432],[116.706691,39.924245],[116.739441,39.684745],[116.815496,39.752241]]
waylist = [[116.681114,39.709432],[116.597232,40.204182],[116.528726,40.011064]]

@app.route('/way')
def waypoints():
    try:
        jsondata = requests.get(
            "https://ae770067-27eb-4c02-b5cd-9620231fb68e.bspapp.com/http/getcarinfo", timeout=3)
        # jsondata = {"affectedDocs":1,"data":[{"_id":"5ff1491323976b00015e89e6","info":{"cartype":"1","province":"黑","
        #             number":"1NE11","height":null,"width":null}}]}
        jsondata = jsondata.replace("\'", "\"")
        print("[*]"+jsondata)
        data = json.loads(jsondata)
        size = data['data'][0]['info']['cartype']
        province = data['data'][0]['info']['province']
        number = data['data'][0]['info']['number']
        load = data['data'][0]['info']['load']
    except:
        size = 4
        province = '黑'
        number = "1NE11"
        load = 15

    rightShift(waylist,1)
    print(waylist)

    print(size, province, number)
    Best_path = [[18], [18, 10, 6, 11, 12], [12], [12], [9, 15, 3, 21], [
        11, 4], [4, 17], [5, 7, 20], [2, 19, 16, 14], [14, 13, 8, 1], [1]]
    return render_template('waypoints.html', province=province, number=number,waylist=waylist,size=size,load=load)


@app.route('/move')
def move():
    plist = []
    jsondata = requests.get("https://ae770067-27eb-4c02-b5cd-9620231fb68e.bspapp.com/http/get")
    jsondata = jsondata.text.replace("\'", "\"")
    print(jsondata)
    data = json.loads(jsondata)
    for point in data['data'][0]['markers']:
        plist.append([float(point['longitude']), float(point['latitude'])])
    print(plist)
    return render_template('move.html', plist=plist)


@app.route('/')
def index():
    return render_template('waypoints.html')


def reverse(arr,start,end):
    while start<end:
        temp = arr[start]
        arr[start] = arr[end]
        arr[end] = temp
        start += 1
        end -= 1

def rightShift(arr,k):
    if arr == None:
        print("参数不合法！")
        return
    lens = len(arr)
    k %= lens
    reverse(arr,0,lens-k-1)
    reverse(arr,lens-k,lens-1)
    reverse(arr,0,lens-1)
