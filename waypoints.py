from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/<cpn>')
def waypoints(cpn):
    cartype = cpn[0]
    province = cpn[1]
    number = cpn[2:]
    print(cartype,province,number)
    Best_path = [[18], [18, 10, 6, 11, 12], [12], [12], [9, 15, 3, 21], [
        11, 4], [4, 17], [5, 7, 20], [2, 19, 16, 14], [14, 13, 8, 1], [1]]
    return render_template('waypoints.html', province=province, number=number)


@app.route('/')
def index():
    return render_template('waypoints.html')
