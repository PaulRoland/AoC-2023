# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 05:50:30 2023

@author: Paul
"""
import time
start_time = time.time_ns()
MEMO = {}
from functools import cache

def get_number_list(lst):
    new_lst = [int(x) for x in lst]
    return new_lst

@cache
def get_permutations(startplek,startgroep,string,numbers):
    permutations=0  
    number=numbers[startgroep]
    #print(string[startplek:],numbers[startgroep:],startplek)
    length = len(string)
    
    #if (startplek,startgroep) in MEMO:
    #   #print("snelweg")
    #   return MEMO[(startplek,startgroep)]
    

    ruimte_nodig = sum(numbers[startgroep:]) + len(numbers[startgroep:])-1
    if startplek+ruimte_nodig > length:
        return 0
    
    for i in range(startplek,len(string)-ruimte_nodig+1): 
        #possible=True
        
        for j in range(number): #Ga alle tekens af om te controleren of daar een ? of een # staat.

            if string[i+j]=='?' or string[i+j]=='#':
                possible=True
            elif string[i+j]=='.':
                #Hij kan hier niet dus we zijn klaar met deze for loop
                possible=False
                break
        #Het waren niet allemaal ? of #, dus we kunnen met verder met een andere i  
        #print(possible)
        if possible==False:
            continue
        #Als hij er kan staan dan moeten we verder zoeken onder bepaalde voorwaardes:
        #eerstvolgende is geen #

        if i+number+1<length:
            if string[i+number]=='#':
                possible=False
  
        if possible==True and '#' not in string[startplek:i]:
            if len(numbers)==startgroep+1: #We zijn bij het laatste getal
                #Check of er geen hashtags meer in het verschiet zijn
                if i+number < length:
                    if '#' not in string[i+number:]:
                        #print("permutatie",i,j,numbers[startgroep:],string[i+number:])
                        permutations +=1
            else: #Er zijn nog nummers over en er is nog ruimte over
                    #print(string[startplek:]," riep een functie aan", string[i+number+1:],numbers[startgroep+1:])
                    permutations=permutations+get_permutations(i+number+1,startgroep+1,string,numbers) #Stuur het overgebleven stuk puzzel door. i+j+2 want er moet ruimte zitten    
    
        if string[i]=='#':
            #Als dit begon met een hashtag dan is het feest nu direct voorbij
            #print("Feest voorbij")
            break
        
    MEMO[(startplek,startgroep)]=permutations
    return permutations

f = open("input_dag12.txt", "r")
total1=0
total2=0
total_list3=list()
for line in f:
    line=line.replace('(','').replace(')','').replace('=','').replace('\n','')
    springs,groups = line.split(' ')
    groups = list(map(int,groups.split(',')))
    springs5=springs+'?'+springs+'?'+springs+'?'+springs+'?'+springs+'.'
    springs=springs+'.'
    groups5=groups*5
    MEMO={}
    total1 = total1 + get_permutations(0,0,springs,groups)
    MEMO={}
    total2 = total2 + get_permutations(0,0,springs5,groups5)
f.close()
 
print("Part 1",total1)
print("Part 2",total2)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
