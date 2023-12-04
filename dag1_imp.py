# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 16:59:03 2023

@author: Paul
"""

#Day 1 part 1
#The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. 
#On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.
import time
start_time = time.time_ns()

def findtext(line,text):
    location=line.find(text)
    if location>-1:
        return location
    return 99999

def find_digit(line,digits): 
    # Zoek de positie van de eerste digit in tekst,of zoek de positie van de eerste digit als digit
    location=99999
    min_location=99999
    first_digit=0
    
    #Itereer over alle items in de digits-dictionary
    for key,num in digits.items():
        if key in line:
            location = findtext(line,key)
        
        #Als de locatie in de string eerder is dan tot nu toe dan gaan we hem onthouden
        if location<min_location:
            min_location=location
            first_digit=num     
            
    return first_digit

f = open("input_dag1.txt", "r")
total1 = 0
total2 = 0
digits1={'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
digits2={'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9}
digits2_rev={'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'eno':1,'owt':2,'eerht':3,'ruof':4,'evif':5,'xis':6,'neves':7,'thgie':8,'enin':9}
for line in f: 
    total1 = total1 + find_digit(line,digits1)*10+find_digit(line[::-1],digits1)
    total2 = total2 + find_digit(line,digits2)*10+find_digit(line[::-1],digits2_rev)
f.close()  

print("Dag 1: Part 1:",total1)
print("Dag 2: Part 2:",total2)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))