import time
import random
import csv
import math
import os.path
from tkinter import *
from functools import partial

##  Initializes the UI/event listeners
def main():
    window = Tk()
    window.title("Merge Sort")

    ##  Listbox labels
    Label(window, text="Unsorted Array").grid(row=1, pady=(12,0), sticky=W)
    Label(window, text="Sorted Array").grid(row=1, column=1, pady=(12,0), sticky=W)

    ##  Create listboxes to display arrays and attach scrollbars
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

    ##  Create user input field and submission button
    Label(window, text="Enter array number (1-9):").grid(row=0)
    entry = Entry(window)
    entry.grid(row=0, column=1)
    Button(window, text="Retrieve and Sort", command=partial(display, entry, listbox1, listbox2)).grid(row=0, column=2)

    ##  Continue to display window until user exits
    window.mainloop()

##  Gets called when a user clicks the "Retrieve and Sort" button
##  Checks that user input is valid and generates/displays results
def display(entry, listbox1, listbox2):
    ##  Make sure the input is an integer
    try:
        size = int(Entry.get(entry))
        entry.delete(0, END)
        
        listbox1.delete(0, END)
        listbox2.delete(0, END)

        ##  Make sure the input integer is in the range 1-9 and generate/display output
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
        ##  If integer not in range 1-9, set output to "Invalid input"
        else:
            listbox1.insert(END, "Invalid input")
            listbox2.insert(END, "Invalid input")
    ##  If input not an integer, set output to "Invalid input"
    except:
        entry.delete(0, END)
        
        listbox1.delete(0, END)
        listbox2.delete(0, END)
        listbox1.insert(END, "Invalid input")
        listbox2.insert(END, "Invalid input")

##  Generate 1000 * size random numbers in an array
def generateNumbers(rangeMin, rangeMax, size):
    array = random.sample(range(rangeMin, rangeMax), size)
    return array

##  Merge the two halves in sorted order
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

##  Split array into halves recursively until subarray size is 1
##  Call merge to merge the two halves
def mergeSort(array, left, right):
    if left < right:
        mid = (left + right)//2

        mergeSort(array, left, mid)
        mergeSort(array, mid+1, right)
        merge(array, left, mid, right)

##  Generates the output spreadsheet
def generateResults(sortedArray, elapsedTime, fileName):
    ##  Calculate values
    n = len(sortedArray)
    
    nlogn = n * (math.log2(n))
    
    timeSpent = str(elapsedTime) + " ms"
    
    x = (nlogn / elapsedTime)
    y = 0
    while x >= 10:
        x = x/10
        y += 1
    x = int(x)
    x = str(x) + '*10^' + str(y)

    ##  If spreadsheet does not already exists, create it and add column headers and results
    if os.path.isfile(fileName) == False:
        with open(fileName, mode='w', newline='') as csv_file:
            fieldnames = ['Input Size n for Array_i', 'Value of n*logn', 'Time Spent (milliseconds)', 'Value of (n*logn)/time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'Input Size n for Array_i': n, 'Value of n*logn': nlogn, 'Time Spent (milliseconds)': timeSpent, 'Value of (n*logn)/time': x})
    ##  If spreadsheet already exists, append results to the existing file
    else:
        with open(fileName, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow((n, nlogn, timeSpent, x))

if __name__ == "__main__":
    main()
