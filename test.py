import requests
import pandas as pd
import time
data = pd.read_excel('./order.xlsx')
print(data)

Best_path = [[1000, 2, 6, 7, 8, 9, 83, 87, 88, 1000], [1000, 4, 17, 3, 14, 15, 16, 93, 112, 1000], [1000, 6, 147, 123, 137, 110, 108, 128, 105, 106, 148, 126, 104, 119, 115, 117, 135, 96, 144, 139, 138, 134, 103, 121, 114, 100, 130, 122, 107, 131, 127, 111, 102, 109, 98, 92, 97, 99, 125, 136, 140, 124, 120, 145, 95, 94, 129, 116, 132, 143, 142, 141, 133, 118, 101, 146, 113, 149, 25, 37, 55, 1000], [1000, 6, 36, 81, 33, 58,
                                                                                                                                                                                                                                                                                                                                                                                                                  29, 56, 39, 43, 78, 57, 35, 75, 61, 44, 31, 67, 42, 34, 38, 28, 59, 40, 71, 48, 62, 45, 70, 26, 50, 68, 52, 41, 64, 72, 27, 77, 60, 79, 65, 74, 49, 80, 51, 53, 73, 30, 69, 76, 1000], [1000, 5, 32, 63, 46, 54, 47, 66, 82, 150, 151, 152, 84, 1000], [1000, 2, 85, 86, 89, 90, 153, 154, 4, 1000], [1000, 2, 5, 18, 19, 20, 21, 155, 156, 157, 158, 91, 1000], [1000, 4, 22, 23, 24, 2, 10, 11, 12, 13, 0, 1000], [1000, 5, 1, 1000]]
lines = [[5, 13, 15], [9, 3, 8, 18], [18, 11, 12], [12], [12, 19, 14],
         [14, 16, 20, 4], [4, 10, 21, 17], [11, 2, 6, 7, 1], [1]]

markers = []
pointdata = {}
id = 0
for idx, line in enumerate(Best_path):
    for place in line:
        pointdata["id"] = id
        # pointdata["name"] =
        # pointdatapointdata["latitude"] =
        # pointdata["latitude"] =
        pointdata["cartype"] = Best_path[idx][1]
        pointdata["createTime"] = time.time()
        id += 1
        markers.append(pointdata)

# jsondata = json.encoder(Best_path)
url = "https://ae770067-27eb-4c02-b5cd-9620231fb68e.bspapp.com/http/add"
data = {"makers": markers, "createTime": time.time()}
print(data)
r = requests.post(url, markers=data)
print(r.text)
