import matplotlib
from flask import Flask, render_template, g
from flask import request
from matplotlib import pyplot as plt

from PastDays import PastDays
from Room import Room
import sqlite3
from datetime import datetime

import subprocess


import time

DATABASE = 'data.sqlite'
app = Flask(__name__)

col = PastDays()

def sortByRoom(room):
    return room.corpus

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def createСhart(data, flag):

    xdata = []
    ydata = []
    for i in data:
        year = int(i[0][:4])
        mon = int(i[0][5:7])
        day = int(i[0][8:10])

        h = i[1] // 60
        m = i[1] % 60

        xdata.append(datetime(year, mon, day, h, m))
        ydata.append(i[2])
    xdata_float = matplotlib.dates.date2num(xdata)
    fig = plt.figure()
    ax = fig.gca()
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
    ax.plot_date(xdata_float, ydata, fmt="b-")
    ax.set_xlabel("Время (час:мин)", fontsize=15)
    if flag:
        fig.suptitle("Температура", fontsize=30)
        ax.set_ylabel("Температура (°C)", fontsize=15)
        fig.savefig('static/1')
    else:
        fig.suptitle("Влажность", fontsize=30)
        ax.set_ylabel("Влажность (%)", fontsize=15)
        fig.savefig('static/2')


@app.route('/')
def hello_world():

    corpus = []

    date = str(datetime.now())[:10]
    time = int(str(datetime.now())[11:13]) * 60 + int(str(datetime.now())[14:16])

    silence = 15


    cur = get_db().cursor()
    cur.execute("SELECT corpus.num_corpus, corpus.fidelio,corpus.room,data.temperature,data.humidity,data.date,max(data.time) FROM corpus, data WHERE data.number = corpus.room and data.date = (SELECT max(date) FROM data) GROUP BY corpus.room")
    data = cur.fetchall()
    for i in data:
        corpus.append(Room(i))
    corpus.sort(key=sortByRoom)

    for i in corpus:
        if i.date == date and i.time + silence < time:
            i.color = "#FF2400"
        elif i.date != date:
            i.color = "#FF2400"
        else:
            i.color = "#FFFFFF"

    return render_template("main.html", corpus = corpus)

@app.route('/setdata/', methods=['GET'])
def setData():

    flag = False

    if request.args['tem'] != "nan":
        flag = True

    if flag:
        time = int(str(datetime.now())[11:13]) * 60 + int(str(datetime.now())[14:16])
        cur = get_db().cursor()

        cur.execute("INSERT INTO data (number, temperature, humidity, date, time) VALUES (?, ?, ?, ?, ?)",
            [int(request.args['room']),
            float(request.args['tem']),
            float(request.args['hum']),
            str(datetime.now())[:10],
            time])

        get_db().commit()
        return 'ok'
    else:
        return 'not ok'

@app.route('/clearingHistory/', methods=['GET'])
def clearingHistory():

    cur = get_db().cursor()
    cur.execute("select * from data")
    data = cur.fetchall()
    col = PastDays()

    acceptableDays = col.getListDate(int(request.args['numberDays']))

    listToDelete = []
    for i in data:
        if i[3] not in acceptableDays:
            listToDelete.append(i[3])

    for i in set(listToDelete):
        cur.execute("delete from data where date = ?", [i])
        get_db().commit()

    return hello_world()



@app.route('/historyRoom/<date>/<number>')
def historyRoom(date, number):
    cur = get_db().cursor()
    listDate = []

    cur.execute("SELECT date, time, temperature FROM data WHERE date = ? AND number = ?", [date, number])
    data = cur.fetchall()
    createСhart(data,True)

    cur.execute("SELECT date, time, humidity FROM data WHERE date = ? AND number = ?", [date, number])
    data = cur.fetchall()
    createСhart(data,False)

    cur.execute("SELECT date FROM data WHERE number = ?", [number])
    data = cur.fetchall()

    for i in data:
        listDate.append(i[0])

    listDate = set(listDate)

    listDate = list(listDate)

    listDate.sort()

    return render_template("historyroom.html", room = number, history = listDate)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()
