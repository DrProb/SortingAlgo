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

def insertionsort(zahlen, balken, start, stop):
    for i in range(start+1, stop):
        while zahlen[i] < zahlen[i-1] and i > start:
            zahlen[i], zahlen[i-1] = zahlen[i-1], zahlen[i]
            i-=1
            if visuals:
                updateBalken(balken, zahlen, i, None)

def timsort(zahlen, balken, start, stop):
    minRun = 32
    runs = []
    while start < stop:
        end = start+minRun
        if end > stop:
            end = stop
        insertionsort(zahlen, balken, start, end)
        runs.append((start, end))
        start = end
    #mergesort(zahlen, balken, 0, stop-1)
    while len(runs) > 1:
        runs2 = []
        for i in range(0, len(runs), 2):
            if i+1 < len(runs):
                merge(zahlen, runs[i][0], runs[i][1]-1, runs[i+1][1]-1)
                runs2.append((runs[i][0], runs[i+1][1]))
            else:
                runs2.append(runs[i])
        runs = runs2


    
def mergesort(zahlen, balken, start, stop):
    if start >= stop:
        return zahlen
    mitte = (start + stop) // 2
    mergesort(zahlen, balken, start, mitte)
    mergesort(zahlen, balken, mitte+1, stop)
    merge(zahlen, start, mitte, stop)
     
def merge(zahlen, start, mitte, stop):
    merged = []
    i = start
    j = mitte+1
    while i <= mitte and j <= stop:
        if zahlen[i] <= zahlen[j]:
            merged.append(zahlen[i])
            i+=1
        else:
            merged.append(zahlen[j])
            j+=1
    for k in range(i, mitte + 1):
        merged.append(zahlen[k])
    for l in range(j, stop):
        merged.append(zahlen[l])
    if visuals:
        for m, zahl in enumerate(merged):
            zahlen[start+m] = zahl
            updateBalken(balken, zahlen, start+m, None)

    

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

def sortedAnimation(balken, zahlen):
    for i in range(0, len(zahlen)+1, 3):
        for j in range(i):
            balk = balken[j]
            balk.set_color("green")
        plt.pause(0.00000000000000000000000000000001)
    for balk in balken:
        balk.set_color("green")            

startZeit = time.perf_counter()
timsort(zahlen, balken, 0, len(zahlen))
endeZeit = time.perf_counter()
if visuals:
    sortedAnimation(balken, zahlen)
print(zahlen)
print(f"Sorting Complete: {endeZeit-startZeit}")

if visuals:
    plt.ioff()
    plt.show()
