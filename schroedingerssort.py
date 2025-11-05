import sqlite3
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import time
import random


connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("SELECT zahlOben FROM daten")
zahlen = [zeile[0] for zeile in cursor.fetchall()]
connection.close()
startZeit = time.time()
visuals = True


def float_to_string(y, egal):
    return (f"{int(y):,}".replace(",", "."))
balken = []
if visuals:
    plt.ion()
    canvas, krd = plt.subplots()
    for x, höhe in enumerate(zahlen):
        balken.append(krd.bar(x, höhe, color= "blue")[0])
    krd.set_ylim(0, 1000000)
    krd.yaxis.set_major_formatter(FuncFormatter(float_to_string))


        

def schroedingerssort(zahlen, balken):
    timeS = time.perf_counter()
    timeE = timeS
    while timeE-timeS<=0.5:
        random.shuffle(zahlen)
        if visuals:
            updateBalken(balken, zahlen, None, None)
        timeE = time.perf_counter()
    if visuals:
        plt.cla()
        plt.text(0.5, 0.5, "?", ha="center", va="center", fontsize=180, color="blue", transform=plt.gca().transAxes)
        plt.axis("off")

        

def updateBalken(balken, zahlen, pivotIdx, compareIdx):
    for i in range(len(zahlen)):
        balk = balken[i]
        zahl = zahlen[i]
        balk.set_height(zahl)
        balk.set_color("blue")
        if i == pivotIdx:
            balk.set_color("red")
        elif i == compareIdx:
            balk.set_color("yellow")
    plt.pause(0.0000000000000000000000000000000000001)

schroedingerssort(zahlen, balken)

if visuals:
    plt.ioff()
    plt.show()
