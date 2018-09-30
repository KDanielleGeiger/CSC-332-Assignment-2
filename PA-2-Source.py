import time
import random
import csv
import math
import os.path
from tkinter import *
from functools import partial

def main():
    window = Tk()
    window.title("Merge Sort")

    Label(window, text="Unsorted Array").grid(row=1, pady=(12,0), sticky=W)
    Label(window, text="Sorted Array").grid(row=1, column=1, pady=(12,0), sticky=W)
    
    listbox1 = Listbox(window, width=20)
    scrollbar1 = Scrollbar(window, orient=VERTICAL)
    listbox1.config(yscrollcommand=scrollbar1.set)
    scrollbar1.config(command=listbox1.yview)
    listbox1.grid(row=2, sticky=W)
    scrollbar1.grid(row=2, sticky=E+NS)

    listbox2 = Listbox(window, width=22)
    scrollbar2 = Scrollbar(window, orient=VERTICAL)
    listbox2.config(yscrollcommand=scrollbar2.set)
    scrollbar2.config(command=listbox2.yview)
    listbox2.grid(row=2, column=1)
    scrollbar2.grid(row=2, column=1, sticky=E+NS)

    Label(window, text="Enter array number (1-9):").grid(row=0)
    entry = Entry(window)
    entry.grid(row=0, column=1)
    Button(window, text="Retrieve and Sort", command=partial(display, entry, listbox1, listbox2)).grid(row=0, column=2)
    
    window.mainloop()

def display(entry, listbox1, listbox2):
    try:
        size = int(Entry.get(entry))
        entry.delete(0, END)
        
        listbox1.delete(0, END)
        listbox2.delete(0, END)
        
        if size in range(1,10):
            array = generateNumbers(-10000, 10000, 1000 * size)
            
            for x in array:
                listbox1.insert(END, x)

            startTime = time.perf_counter()
            mergeSort(array, 0, len(array) - 1)
            elapsedTime = round(((time.perf_counter() - startTime) * 1000), 6)

            for x in array:
                listbox2.insert(END, x)
               
            generateResults(array, elapsedTime, "Mergesort_Time.csv")
        else:
            listbox1.insert(END, "Invalid input")
            listbox2.insert(END, "Invalid input")
    except:
        entry.delete(0, END)
        
        listbox1.delete(0, END)
        listbox2.delete(0, END)
        listbox1.insert(END, "Invalid input")
        listbox2.insert(END, "Invalid input")

def generateNumbers(rangeMin, rangeMax, size):
    array = random.sample(range(rangeMin, rangeMax), size)
    return array

def merge(array, left, mid, right):
    leftHalf = array[left:mid+1]
    rightHalf = array[mid+1:right+1]

    i = 0
    j = 0
    k = left
    while i < len(leftHalf) and j < len(rightHalf):
        if leftHalf[i] <= rightHalf[j]:
            array[k] = leftHalf[i]
            i += 1
        else:
            array[k] = rightHalf[j]
            j += 1
        k += 1

    while i < len(leftHalf):
        array[k] = leftHalf[i]
        i += 1
        k += 1

    while j < len(rightHalf):
        array[k] = rightHalf[j]
        j += 1
        k += 1

def mergeSort(array, left, right):
    if left < right:
        mid = (left + right)//2

        mergeSort(array, left, mid)
        mergeSort(array, mid+1, right)
        merge(array, left, mid, right)

def generateResults(sortedArray, elapsedTime, fileName):
    n = len(sortedArray)
    
    nlogn = n * (math.log10(n))
    
    timeSpent = str(elapsedTime) + " ms"
    
    x = (nlogn / elapsedTime)
    y = 0
    while x >= 10:
        x = x/10
        y += 1
    x = int(x)
    x = str(x) + '*10^' + str(y)

    
    if os.path.isfile(fileName) == False:
        with open(fileName, mode='w', newline='') as csv_file:
            fieldnames = ['Input Size n for Array_i', 'Value of n*logn', 'Time Spent (milliseconds)', 'Value of (n*logn)/time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'Input Size n for Array_i': n, 'Value of n*logn': nlogn, 'Time Spent (milliseconds)': timeSpent, 'Value of (n*logn)/time': x})
    else:
        with open(fileName, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow((n, nlogn, timeSpent, x))

if __name__ == "__main__":
    main()
