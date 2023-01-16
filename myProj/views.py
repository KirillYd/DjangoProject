from django.http import HttpResponse
from django.shortcuts import render
import program
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

from myProj import aaa


def index_view(request):
    return render(request, 'index.html')


def postuser(request):
    x1 = int(request.POST.get("x1"))
    x2 = int(request.POST.get("x2"))
    y1 = int(request.POST.get('y1'))
    y2 = int(request.POST.get('y2'))
    coord(x1, y1, x2, y2)

    return render(request, 'index.html', {"graph": "img/photo.png"})

def coord(x1,y1,x2,y2):
    objs = program.get_objs()
    line = program.Line(program.Point(x1, y1), program.Point(x2, y2))

    x = np.array([line.point1.x, line.point2.x])
    y = np.array([line.point1.y, line.point2.y])

    a = []
    for data in objs.values():
        a.append(len(data))
    max_a = max(a)
    print(max_a)

    id_crossing = []
    cnt = 0

    time_list = []
    person_cnt = []

    c_dict = {}  ###
    for track_id in objs.keys():
        r = []
        for point in objs[track_id]:
            new_list = [line.is_point_above_line(point[0]), point[1]]
            r.append(new_list)
            if point[1] not in c_dict:
                c_dict[point[1]] = 0

        for i in range(len(r) - 1):
            if r[i][0] != r[i + 1][0] and r[i][0] == True:
                cnt += 1
                id_crossing.append(i)
                time_list.append([datetime.now(), cnt])
                c_dict[r[i][1]] = cnt
            elif r[i][0] != r[i + 1][0] and r[i][0] == False:
                cnt -= 1
                time_list.append([datetime.now(), cnt])
                c_dict[r[i][1]] = cnt
            else:
                c_dict[r[i][1]] = cnt

    # Временой ряд
    df = pd.DataFrame({'time': np.array([key for key in c_dict.keys()]), 'cnt': [value for value in c_dict.values()]})
    plt.figure(figsize=(20, 5))
    plt.plot(df.time, df.cnt, linewidth=1)
    plt.savefig('myProj/static/img/photo.png', dpi=100)

    # отображение траекторий посетителей
    plt.imshow(program.first_img)
    for k, v in objs.items():
        xs, ys = [], []
        for po in v:
            xs.append(po[0].x)
            ys.append(po[0].y)
        plt.plot(xs, ys)
    plt.plot(x, y, color='r')
    plt.savefig('myProj/static/img/trajectory.png', dpi=100)





# Create your views here.
