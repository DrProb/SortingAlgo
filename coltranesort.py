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
    plt.style.use("dark_background")

    canvas, krd = plt.subplots()
    #plt.style.use("dark_background")


    for x, höhe in enumerate(zahlen):
        balken.append(krd.bar(x, höhe, color= "blue")[0])
    krd.set_ylim(0, 1000000)
    krd.yaxis.set_major_formatter(FuncFormatter(float_to_string))

def aufteilen(zahlen, balken, start, stop, timeS):
    pivot = zahlen[stop]
    nextKleiner = start
    for i in range(start, stop):
        if zahlen[i] <= pivot:
            zahlen[nextKleiner], zahlen[i] = zahlen[i], zahlen[nextKleiner]
            if visuals:
                 updateBalken(balken, zahlen, stop, i)
            nextKleiner += 1
            timeE = time.perf_counter()
            if timeE-timeS > 0.5:
                return
    zahlen[nextKleiner], zahlen[stop] = zahlen[stop], zahlen[nextKleiner]
    if visuals:
        updateBalken(balken, zahlen, nextKleiner, None)
    return nextKleiner

def quicksort(zahlen, balken, start, stop, timeS):
    timeE = timeS
    if start < stop:
        pivotIdx = aufteilen(zahlen, balken, start, stop, timeS)
        timeE = time.perf_counter()
        if timeE-timeS > 0.5:
            return
        quicksort(zahlen, balken, start, pivotIdx-1, timeS)
        timeE = time.perf_counter()
        if timeE-timeS > 0.5:
            return
        quicksort(zahlen, balken, pivotIdx+1, stop, timeS)
        timeE = time.perf_counter()
        if timeE-timeS > 0.5:
            return

def heap(zahlen, balken, stop, i, timeS):
    timeE = timeS
    groesstes = i
    childLinks = 2*i + 1
    childRechts = 2*i + 2
    if childLinks < stop and zahlen[childLinks] > zahlen[groesstes]:
        groesstes = childLinks
    if childRechts < stop and zahlen[childRechts] > zahlen[groesstes]:
        groesstes = childRechts
    if visuals:
        updateBalken(balken, zahlen, groesstes, stop)
    if groesstes != i:
        zahlen[i], zahlen[groesstes] = zahlen[groesstes], zahlen[i]
        if visuals:
            updateBalken(balken, zahlen, groesstes, stop)
        timeE = time.perf_counter()
        if timeE-timeS > 0.5:
            return
        heap(zahlen,balken, stop, groesstes, timeS)

def insertionsort(zahlen, balken, stop, timeS):
    timeE = timeS
    for i in range(1, stop):
        while zahlen[i] < zahlen[i-1] and i > 0:
            zahlen[i], zahlen[i-1] = zahlen[i-1], zahlen[i]
            i-=1
            if visuals:
                updateBalken(balken, zahlen, i, None)
            timeE = time.perf_counter()
            if timeE-timeS > 0.5:
                return

def mergesort(zahlen, balken, start, stop, timeS):
    if start >= stop:
        return zahlen
    mitte = (start + stop) // 2
    mergesort(zahlen, balken, start, mitte, timeS)
    timeE = time.perf_counter()
    if timeE-timeS > 0.5:
        return
    mergesort(zahlen, balken, mitte+1, stop, timeS)
    timeE = time.perf_counter()
    if timeE-timeS > 0.5:
        return
    merge(zahlen, start, mitte, stop, timeS)
    timeE = time.perf_counter()
    if timeE-timeS > 0.5:
        return
     
def merge(zahlen, start, mitte, stop, timeS):
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
        timeE = time.perf_counter()
        if timeE-timeS > 0.5:
            return
    for k in range(i, mitte + 1):
        merged.append(zahlen[k])
    for l in range(j, stop):
        merged.append(zahlen[l])
    if visuals:
        for m, zahl in enumerate(merged):
            zahlen[start+m] = zahl
            updateBalken(balken, zahlen, start+m, None)

def sleepsort(zahlen, balken, stop, timeS):
    sorted = []
    i = 0
    timeE = timeS
    while len(sorted) < stop:
        sortedIdxs = []
        for j, zahl in enumerate(zahlen):
            if zahl == i:
                sorted.append(zahl)
                sortedIdxs.append(j)
        for idx in sortedIdxs:
            zahlen.pop(idx)
            zahlen.insert(len(sorted)-1, i)
            if visuals:
                updateBalken(balken, zahlen, len(sorted)-1, None)
        i += 1
        timeE = time.perf_counter()
        if timeE-timeS > 0.5:
            return

def sorted(zahlen, balken):
    #if visuals:
     #   updateBalken(balken, zahlen, None, None)
    for i in range(len(zahlen)-1):
        if zahlen[i] > zahlen[i+1]:
            #if visuals:
                #updateBalken(balken, zahlen, None, None)
            return False
    return True

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

def selectionsort(zahlen, balken, stop, timeS):
    for count in range(stop):
        smallestIdx = count
        for i in range(count, stop):
            if zahlen[smallestIdx] > zahlen[i]:
                smallestIdx = i
            if visuals:
                updateBalken(balken, zahlen, smallestIdx, i)

        zahlen[count], zahlen[smallestIdx] = zahlen[smallestIdx], zahlen[count]    
        timeE = time.perf_counter()
        if timeE-timeS > 0.5:
            return

def coltranesort(zahlen, balken, stop):
    timeDif = 1
    while not sorted(zahlen, balken):
        timeS = time.perf_counter()
        currentSort = random.randint(0, 5)
        #print(f"New Sorting Algo: {currentSort}")
        if currentSort == 0:
            bogosort(zahlen, balken, timeS)
        elif currentSort == 1:
            bubblesort(zahlen, balken, stop-1, timeS)
        elif currentSort == 2:
            heapsort(zahlen, balken, stop, timeS)
        elif currentSort == 3:
            insertionsort(zahlen, balken, stop, timeS)
        elif currentSort == 4:
            sleepsort(zahlen, balken, stop, timeS)
        elif currentSort == 5:
            quicksort(zahlen, balken, 0, stop-1, timeS)
        



def heapsort(zahlen, balken, stop, timeS):
    i = (stop-1)//2
    timeE = timeS
    while i >= 0:
        heap(zahlen, balken, stop, i, timeS)
        timeE = time.perf_counter()
        if timeE-timeS > 0.5:
            return
        i -= 1
    while stop>0:
        stop-=1
        zahlen[0], zahlen[stop] = zahlen[stop], zahlen[0]
        heap(zahlen, balken, stop, 0, timeS)
        timeE = time.perf_counter()
        if timeE-timeS > 0.5:
            return

def bogosort(zahlen, balken, timeS):
    timeE = timeS
    while not sorted(zahlen, balken) and timeE-timeS<=0.5:
        random.shuffle(zahlen)
        if visuals:
            updateBalken(balken, zahlen, None, None)
        timeE = time.perf_counter()

def bubblesort(zahlen, balken, count, timeS):
    timeE=timeS
    while count > 0:
        for i in range(count):
            if zahlen[i] > zahlen[i+1]:
                zahlen[i], zahlen[i+1] = zahlen[i+1], zahlen[i]
                if visuals:
                    updateBalken(balken, zahlen, None, i+1)
                timeE = time.perf_counter()
                if timeE-timeS > 0.5:
                    return
        count -= 1

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
coltranesort(zahlen, balken, len(zahlen))
endeZeit = time.perf_counter()
if visuals:
    sortedAnimation(balken, zahlen)
print(zahlen)
print(f"Sorting Complete: {endeZeit-startZeit}")

if visuals:
    plt.ioff()
    plt.show()
