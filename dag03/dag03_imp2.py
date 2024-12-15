# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 06:41:28 2023

@author: Paul
"""
import numpy as np
import time
start_time = time.time_ns()

def check_lijn(lijn):
    n=0
    waarde = 1
    if lijn[2].isdigit(): #getal linksboven
        if lijn[3].isdigit(): #getal linksboven en direct boven de gear
            if lijn[4].isdigit():
                #3 getallen boven de gear. Geen andere opties meer
                waarde= int(lijn[2:5])
                return [1,waarde]
            
            #geen 3e getal rechtsboven de gear, maar misschien nog wel eentje naar links 
            if lijn[1].isdigit():
                waarde = int(lijn[1:4])
                return [1,waarde]
                       
            #linksboven en boven de gear een getal en rechts boven niet, we zijn klaar met de bovenkant checken. Geen andere opties meer.
            waarde =int(lijn[2:4])
            return [1,waarde] #getal linksboven en boven gear, dus max 1 getal mogelijk.
        #Wel een getal linksboven, maar niet boven de gear
        if lijn[1].isdigit():
            if lijn[0].isdigit():
                waarde = int(lijn[0:3]) #drie getallen
                n=1
            else:
                waarde = int(lijn[1:3]) #twee getallen
                n=1
        else:
            waarde = int(lijn[2]) #1 getal
            n=1
    
    #Hier komen we alleen als linksboven geen waarde heeft of wel een waarde heeft maar het getal daarnaast (rechtstreeks boven de gear) niet.
    if lijn[3].isdigit():
        #getal boven de gear
        #kijk naar rechts vanaf midden
        if lijn[4].isdigit():
            if lijn[5].isdigit():
                waarde=waarde*int(lijn[3:6])
                return [n+1,waarde]
                return [1,int(lijn[3:6])] #3 getallen vanaf recht boven gear
            return [n+1,int(lijn[3:5])] #2 getallen vanaf recht boven gear
        waarde=waarde*int(lijn[3]) #1 getal boven de gear
        return [n+1,waarde]
    
    #hier komen we alleen als linksboven en rechtboven de gear geen getallen zijn.
    if lijn[4].isdigit():
        if lijn[5].isdigit():
            if lijn[6].isdigit():
                return [n+1,waarde*int(lijn[4:])]
            return [n+1,waarde*int(lijn[4:6])]
        return [n+1,waarde*int(lijn[4])]

    return [n,waarde]        


def find_symbol(zoekgebied): 
    zoek_string = zoekgebied[0]+zoekgebied[1]+zoekgebied[2]
    for c in zoek_string:
        if c.isdigit()==False and c!='.':
            return 1;
    return 0

def find_gear_values(zoekgebied):
    n=0
    waarde = 1
    #we kijken links
    if zoekgebied[1][2].isdigit():
        if zoekgebied[1][1].isdigit():
            if zoekgebied[1][0].isdigit():
                gevonden=int(zoekgebied[1][0:3])
            else:        
                gevonden=int(zoekgebied[1][1:3])
        else:
            gevonden=int(zoekgebied[1][2])
        n=n+1
        waarde=waarde*gevonden

    #we kijken rechts
    if zoekgebied[1][4].isdigit():
        if zoekgebied[1][5].isdigit():
            if zoekgebied[1][6].isdigit():
               gevonden=int(zoekgebied[1][4:])
            else:
               gevonden=int(zoekgebied[1][4:6])
        else:
            gevonden=int(zoekgebied[1][4])
        n=n+1
        waarde=waarde*gevonden
    
    #Kijken aan de bovenkant (zelfde als kijken aan de onderkant)
    [_n,_waarde] = check_lijn(zoekgebied[0])
    n=n+_n
    waarde=waarde*_waarde
    
    #Kijken aan de onderkant (zelfde als kijken aan de onderkant)
    [_n,_waarde] = check_lijn(zoekgebied[2])
    n=n+_n
    waarde=waarde*_waarde    

    #Alleen als er twee waardes zijn dan wil ik een output, anders 0
    if n==2:
        return waarde
    return 0


line_empty='...................................................................................................................................................'
check_line=line_empty
line_buffer3=check_line

som_part1=0
som_part2=0
f = open("input_dag3.txt", "r")
for i,line in enumerate(f):
    line_buffer1=check_line
    check_line=line_buffer3
    line_buffer3='...'+line.replace('\n','')+'...'
    for j,letter in enumerate(check_line):        
        if letter.isdigit():
            if check_line[j-1].isdigit()==False:
                #eerste getal van dit nummer
                if check_line[j+1].isdigit():
                    if check_line[j+2].isdigit():
                        zoekgebied=[line_buffer1[j-1:j+4],check_line[j-1:j+4],line_buffer3[j-1:j+4]]
                        som_part1=som_part1+int(check_line[j:j+3])*find_symbol(zoekgebied)#3 getallen
                        continue
                    zoekgebied=[line_buffer1[j-1:j+3],check_line[j-1:j+3],line_buffer3[j-1:j+3]]
                    som_part1=som_part1+int(check_line[j:j+2])*find_symbol(zoekgebied)#2 getallen
                    continue
                zoekgebied=[line_buffer1[j-1:j+2],check_line[j-1:j+2],line_buffer3[j-1:j+2]]
                som_part1=som_part1+int(check_line[j])*find_symbol(zoekgebied)#1 getal
                
        if letter =='*': #als het een gear is dan gaan we kijken rond de gear:
            zoekgebied=[line_buffer1[j-3:j+4],check_line[j-3:j+4],line_buffer3[j-3:j+4]]
            som_part2=som_part2+find_gear_values(zoekgebied) #Geeft de vermenigvuldiging van 2 getallen rond de gear, alleen als er 2 getallen zijn


#check ook de laatste regel
line_buffer1=check_line
check_line=line_buffer3
line_buffer3=line_empty
for j,letter in enumerate(check_line):        
    if letter.isdigit():
        if check_line[j-1].isdigit()==False:
            #eerste getal van dit nummer
            if check_line[j+1].isdigit():
                if check_line[j+2].isdigit():
                    zoekgebied=[line_buffer1[j-1:j+4],check_line[j-1:j+4],line_buffer3[j-1:j+4]]
                    som_part1=som_part1+int(check_line[j:j+3])*find_symbol(zoekgebied)#3 getallen
                    continue
                zoekgebied=[line_buffer1[j-1:j+3],check_line[j-1:j+3],line_buffer3[j-1:j+3]]
                som_part1=som_part1+int(check_line[j:j+2])*find_symbol(zoekgebied)#2 getallen
                continue
            zoekgebied=[line_buffer1[j-1:j+2],check_line[j-1:j+2],line_buffer3[j-1:j+2]]
            som_part1=som_part1+int(check_line[j])*find_symbol(zoekgebied)#1 getal
            
    if letter =='*': #als het een gear is dan gaan we kijken rond de gear:
        zoekgebied=[line_buffer1[j-3:j+4],check_line[j-3:j+4],line_buffer3[j-3:j+4]]
        som_part2=som_part2+find_gear_values(zoekgebied) #Geeft de vermenigvuldiging van 2 getallen rond de gear, alleen als er 2 getallen zijn

    
f.close()   
print(som_part1)
print(som_part2)

#print("Part 1: ",int(total))
#print("Part 2: ",int(np.sum(gear_map * (adj_map==2))))
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
