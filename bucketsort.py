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

def insertionsortVis(zahlenn, balken, start, stop):
    for i in range(start+1, stop):
        while zahlenn[i] < zahlenn[i-1] and i > start:
            zahlenn[i], zahlenn[i-1] = zahlenn[i-1], zahlenn[i]
            i-=1
            if visuals:
                updateBalken(balken, zahlenn, -1, None)

def insertionsort(zahlen, balken, stop):
    for i in range(1, stop):
        while zahlen[i] < zahlen[i-1] and i > 0:
            zahlen[i], zahlen[i-1] = zahlen[i-1], zahlen[i]
            i-=1
            if visuals:
                updateBalken(balken, zahlen, i, None)

def bucketsort(zahlen, balken, stop):
    if stop > 1:
        max = zahlen[0]
        min = zahlen[0]
        for zahl in zahlen:
            if zahl > max:
                max = zahl
            elif zahl < min:
                min = zahl
        rangee = max-min
        buckets = stop
        bucketList = [[] for i in range(buckets)]
        if visuals:
            fakezahlen = zahlen.copy()
            for i, zahl in enumerate(fakezahlen):
                fakezahlen[i] = 0
                updateBalken(balken, fakezahlen, -1, None)
        for i, zahl in enumerate(zahlen):
            normalized = (zahl-min) / rangee
            bucketIdx = int(normalized*(buckets-1))
            bucketList[bucketIdx].append(zahl)
        if visuals:
            output = []
            for bucket in bucketList:
                for zahl in bucket:
                    output.append(zahl)
            if visuals:
                fakeoutput = [0 for i in range(stop)]
                for zahl in zahlen:
                    idx = output.index(zahl)
                    fakeoutput[idx] = zahl
                    updateBalken(balken, fakeoutput, -1, None)
        if visuals:
            i = 0
            for bucket in bucketList:
                insertionsortVis(output, balken, i, i+len(bucket))
                i += len(bucket)
            return output
            
        else:
            for bucket in bucketList:
                bucket = insertionsort(bucket, balken, len(bucket))
            output = []
            for bucket in bucketList:
                for zahl in bucket:
                    output.append(zahl)
            return output

        
            


def updateBalken(balken, zahlen, pivotIdx, compareIdx):
    for i in range(len(zahlen)):
        balk = balken[i]
        zahl = zahlen[i]
        balk.set_height(zahl)
        balk.set_color("blue")
        if i <= pivotIdx:
            balk.set_color("green")
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
zahlen = bucketsort(zahlen, balken, len(zahlen))
endeZeit = time.perf_counter()
if visuals:
    sortedAnimation(balken, zahlen)
print(zahlen)
print(f"Sorting Complete: {endeZeit-startZeit}")

if visuals:
    plt.ioff()
    plt.show()
