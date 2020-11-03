from typing import Optional

from fastapi import FastAPI

import GA_TSP

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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/ping")
def ping():
    return {"pong"}
