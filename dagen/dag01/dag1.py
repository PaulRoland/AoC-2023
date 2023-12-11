# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 16:59:03 2023

@author: Paul
"""

#Day 1 part 1
#The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. 
#On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.
def print_line(line,digit1,digit2):
    print(line[:-1] + "     =>"+ str(digit1)+ " & "+ str(digit2) +"    =>   "+ str(digit1*10+digit2))

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
        location = findtext(line,key)
        
        #Als de locatie in de string eerder is dan tot nu toe dan gaan we hem onthouden
        if location<min_location:
            min_location=location
            first_digit=num     
            
    return first_digit
    


f = open("input_dag1.txt", "r")
total = 0 
digits={'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
for line in f: 
    first_digit = find_digit(line,digits)
    last_digit = find_digit(line[::-1],digits)
    total = total + first_digit*10+last_digit
    #print_line(line,first_digit,last_digit)
f.close()  
print(total)

print("\n\nYour calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid 'digits'.")
print("Equipped with this new information, you now need to find the real first and last digit on each line")

f = open("input_dag1.txt", "r")
total = 0 

digits={'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9}
digits_rev={'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'eno':1,'owt':2,'eerht':3,'ruof':4,'evif':5,'xis':6,'neves':7,'thgie':8,'enin':9}
for line in f:
    first_digit=find_digit(line,digits)
    last_digit=find_digit(line[::-1],digits_rev)
    #print_line(line,first_digit,last_digit)
    total = total + first_digit*10+last_digit
print(total)
f.close()
