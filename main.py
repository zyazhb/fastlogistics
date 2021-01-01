from typing import Optional

from fastapi import FastAPI

import GA_TSP
import json

import requests
import time

app = FastAPI()

mapkey = "510032adf681277699fd944dce14365f"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/map")
def getmap(markers="mid,0xFF0000,A:116.37359,39.92437;116.47359,39.92437"):
    return "https://restapi.amap.com/v3/staticmap?markers="+markers+"&key="+mapkey


@app.get("/tsp")
def tsp():
    markers = "mid,0xFF0000,A:"
    X, Y = GA_TSP.main()
    for i in range(0, len(X)):
        markers += str(X[i])+","+str(Y[i])+";"
    return "https://restapi.amap.com/v3/staticmap?markers="+markers[:-1]+"&key="+mapkey


'''
一共需要12辆车
第0种类型的车,路径为0->[21, 4]->0,运输的商品为[155, 156, 157, 158, 4, 5]
第1种类型的车,路径为0->[5, 16, 17]->0,运输的商品为[6, 7, 8, 9, 89, 90, 91]
第3种类型的车,路径为0->[10, 7, 15, 18]->0,运输的商品为[18, 19, 20, 21, 11, 12, 13, 87, 88, 94, 122, 112, 128, 133, 101, 127, 99, 131, 137]
第4种类型的车,路径为0->[18]->0,运输的商品为[147, 114, 141, 117, 139, 111, 145, 129, 104, 119, 144, 105, 135, 136, 95, 98, 130, 142, 124, 121, 125, 109, 134, 102, 126, 118, 97, 132, 140, 113, 96, 108, 146, 92, 103, 107]
第2种类型的车,路径为0->[18]->0,运输的商品为[106, 115, 93, 148, 123, 143, 110, 100, 116]
第0种类型的车,路径为0->[18, 3, 8, 19]->0,运输的商品为[138, 120, 149, 3, 14, 15, 16, 150, 151, 152]
第0种类型的车,路径为0->[20]->0,运输的商品为[153]
第3种类型的车,路径为0->[20, 6, 14]->0,运输的商品为[154, 10, 84]
第6种类型的车,路径为0->[14, 11]->0,运输的商品为[85, 86, 22, 23, 24]
第3种类型的车,路径为0->[9, 13, 2, 11, 12]->0,运输的商品为[17, 83, 2, 25, 45, 29, 37, 75, 34, 78, 27, 76, 69, 55, 44, 60, 38, 77, 26, 64]
第6种类型的车,路径为0->[12, 1]->0,运输的商品为[46, 40, 70, 36, 67, 54, 71, 43, 59, 50, 35, 58, 47, 61, 49, 68, 32, 62, 56, 33, 41, 65, 63, 31, 28, 80, 39, 81, 48, 74, 66, 30, 73, 42, 53, 72, 52, 51, 79, 57, 82, 0]
第1种类型的车,路径为0->[1]->0,运输的商品为[1]
最低成本为479.8706484316134
[[1000, 0, 155, 156, 157, 158, 4, 5, 1000], [1000, 1, 6, 7, 8, 9, 89, 90, 91, 1000], [1000, 3, 18, 19, 20, 21, 11, 12, 13, 87, 88, 94, 122, 112, 128, 133, 101, 127, 99, 131, 137, 1000], [1000, 4, 147, 114, 141, 117, 139, 111, 145, 129, 104, 119, 144, 105, 135, 136, 95, 98, 130, 142, 124, 121, 125, 109, 134, 102, 126, 118, 97, 132, 140, 113, 96, 108, 146, 92, 103, 107, 1000], [1000, 2, 106, 115, 93, 148, 123, 143, 110, 100, 116, 1000], [1000, 0, 138, 120, 149, 3, 14, 15, 16, 150, 151, 152, 1000], [1000, 0, 153, 1000], [1000, 3, 154, 10, 84, 1000], [1000, 6, 85, 86, 22, 23, 24, 1000], [1000, 3, 17, 83, 2, 25, 45, 29, 37, 75, 34, 78, 27, 76, 69, 55, 44, 60, 38, 77, 26, 64, 1000], [1000, 6, 46, 40, 70, 36, 67, 54, 71, 43, 59, 50, 35, 58, 47, 61, 49, 68, 32, 62, 56, 33, 41, 65, 63, 31, 28, 80, 39, 81, 48, 74, 66, 30, 73, 42, 53, 72, 52, 51, 79, 57, 82, 0, 1000], [1000, 1, 1, 1000]]
[[1000, 0, 155, 156, 157, 158, 4, 5, 1000], [1000, 1, 6, 7, 8, 9, 89, 90, 91, 1000], [1000, 3, 18, 19, 20, 21, 11, 12, 13, 87, 88, 94, 122, 112, 128, 133, 101, 127, 99, 131, 137, 1000], [1000, 4, 147, 114, 141, 117, 139, 111, 145, 129, 104, 119, 144, 105, 135, 136, 95, 98, 130, 142, 124, 121, 125, 109, 134, 102, 126, 118, 97, 132, 140, 113, 96, 108, 146, 92, 103, 107, 1000], [1000, 2, 106, 115, 93, 148, 123, 143, 110, 100, 116, 1000], [1000, 0, 138, 120, 149, 3, 14, 15, 16, 150, 151, 152, 1000], [1000, 0, 153, 1000], [1000, 3, 154, 10, 84, 1000], [1000, 6, 85, 86, 22, 23, 24, 1000], [1000, 3, 17, 83, 2, 25, 45, 29, 37, 75, 34, 78, 27, 76, 69, 55, 44, 60, 38, 77, 26, 64, 1000], [1000, 6, 46, 40, 70, 36, 67, 54, 71, 43, 59, 50, 35, 58, 47, 61, 49, 68, 32, 62, 56, 33, 41, 65, 63, 31, 28, 80, 39, 81, 48, 74, 66, 30, 73, 42, 53, 72, 52, 51, 79, 57, 82, 0, 1000], [1000, 1, 1, 1000]]
'''


@app.get("/calc")
def calc():
    import calc
    markers = "mid,0xFF0000,A:"
    Best_path, lines = calc.main()
    print(Best_path, lines)
    url = "https://ae770067-27eb-4c02-b5cd-9620231fb68e.bspapp.com/"
    data = {"creatTime": time.now(), "makers": Best_path}
    requests.post(url, data=data)
    return data
    # for i in range(0, len(X)):
    #     markers += str(X[i])+","+str(Y[i])+";"
    # return "https://restapi.amap.com/v3/staticmap?markers="+markers[:-1]+"&key="+mapkey


@app.get("/testpost")
def testpost():
    import pandas as pd
    data = pd.read_excel('./order.xlsx')
    print(data)

    Best_path = [[18], [18, 10, 6, 11, 12], [12], [12], [9, 15, 3, 21], [
        11, 4], [4, 17], [5, 7, 20], [2, 19, 16, 14], [14, 13, 8, 1], [1]]

    dictdata = {}
    for idx, line in enumerate(Best_path):
        for place in line:
            dictdata["id"] = idx
            # dictdata["name"] =
            # dictdata["latitude"] =
            # dictdata["latitude"] =
            dictdata["cartype"] = Best_path[idx][1]
            dictdata["createTime"] = time.time()

    # jsondata = json.encoder(Best_path)
    url = "https://ae770067-27eb-4c02-b5cd-9620231fb68e.bspapp.com/http/add"
    # data = {"makers": str(Best_path)}
    r = requests.post(url, data=dictdata)
    return data


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/ping")
def ping():
    return {"pong"}
