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

def sorted(zahlen, balken):
    if visuals:
        updateBalken(balken, zahlen, None, None, 0)
    for i in range(len(zahlen)-1):
        if zahlen[i] > zahlen[i+1]:
            if visuals:
                updateBalken(balken, zahlen, None, None, i)
            return False
    return True
        

def bogosort(zahlen, balken):
    while not sorted(zahlen, balken):
        random.shuffle(zahlen)
        if visuals:
            updateBalken(balken, zahlen, None, None, -1)

        

def updateBalken(balken, zahlen, pivotIdx, compareIdx, richtige):
    for i in range(len(zahlen)):
        balk = balken[i]
        zahl = zahlen[i]
        balk.set_height(zahl)
        balk.set_color("blue")
        if i <= richtige:
            balk.set_color("green")
        if i == pivotIdx:
            balk.set_color("red")
        elif i == compareIdx:
            balk.set_color("yellow")
    plt.pause(0.0000000000000000000000000000000000001)

def sortedAnimation(balken, zahlen):
    for i in range(0, len(zahlen)+1, 3):
        for j in range(i):
            balk = balken[j]
            balk.set_color("green")
        plt.pause(0.00000000000000000000000000000001)
    for balk in balken:
        balk.set_color("green")
            

startZeit = time.perf_counter()
bogosort(zahlen, balken)
endeZeit = time.perf_counter()
#if visuals:
 #   sortedAnimation(balken, zahlen)
print(zahlen)
print(f"Sorting Complete: {endeZeit-startZeit}")

if visuals:
    plt.ioff()
    plt.show()
