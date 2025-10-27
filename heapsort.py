import sqlite3
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import time


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


def heap(zahlen, balken, stop, i):
    groesstes = i
    childLinks = 2*i + 1
    childRechts = 2*i + 2
    if childLinks < stop and zahlen[childLinks] > zahlen[groesstes]:
        groesstes = childLinks
    if childRechts < stop and zahlen[childRechts] > zahlen[groesstes]:
        groesstes = childRechts
    if visuals:
        updateBalken(balken, zahlen, i, groesstes, stop)
    if groesstes != i:
        zahlen[i], zahlen[groesstes] = zahlen[groesstes], zahlen[i]
        if visuals:
            updateBalken(balken, zahlen, i, groesstes, stop)
        heap(zahlen,balken, stop, groesstes)


def heapsort(zahlen, balken, stop):
    i = (stop-1)//2
    while i >= 0:
        heap(zahlen, balken, stop, i)
        i -= 1
    while stop>0:
        stop-=1
        zahlen[0], zahlen[stop] = zahlen[stop], zahlen[0]
        heap(zahlen, balken, stop, 0)
        

def updateBalken(balken, zahlen, pivotIdx, compareIdx, sorted):
    for i in range(len(zahlen)):
        balk = balken[i]
        zahl = zahlen[i]
        balk.set_height(zahl)
        balk.set_color("blue")
        if i >= sorted:
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
heapsort(zahlen, balken, len(zahlen))
endeZeit = time.perf_counter()
print(zahlen)
print(f"Sorting Complete: {endeZeit-startZeit}")

if visuals:
    plt.ioff()
    plt.show()
