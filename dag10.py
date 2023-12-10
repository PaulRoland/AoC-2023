# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 05:58:12 2023

@author: Paul
"""

import time
start_time = time.time_ns()
import numpy as np
def get_number_list(lst):
    new_lst = [int(x) for x in lst]
    return new_lst

def next_step(cur_pipe,cur_loc,prev_loc):
    if cur_pipe=='|':
        if prev_loc[1] < cur_loc[1]: #Verticale pijp omlaag
            return ([cur_loc[0],cur_loc[1]+1],cur_loc) #return new location and the new previous location
        return ([cur_loc[0],cur_loc[1]-1],cur_loc) #return new location and the new previous location       
     
    if cur_pipe=='-':
        if prev_loc[0] < cur_loc[0]: #Horizontale pijp naar rechts
            return ([cur_loc[0]+1,cur_loc[1]],cur_loc)
        return ([cur_loc[0]-1,cur_loc[1]],cur_loc) #naar links
     
    if cur_pipe=='L':
          if prev_loc[0] > cur_loc[0]: #Pijp loopt naar boven
              return ([cur_loc[0],cur_loc[1]-1],cur_loc)
          return ([cur_loc[0]+1,cur_loc[1]],cur_loc) #pijp loopt naar beneden
         
    if cur_pipe=='J':
        if prev_loc[0] < cur_loc[0]: #We komen van links
            return ([cur_loc[0],cur_loc[1]-1],cur_loc)
        return ([cur_loc[0]-1,cur_loc[1]],cur_loc)
      
    if cur_pipe=='7':
        if prev_loc[0] < cur_loc[0]: #We komen van links
            return ([cur_loc[0],cur_loc[1]+1],cur_loc)
        return ([cur_loc[0]-1,cur_loc[1]],cur_loc)
      
    if cur_pipe=='F':
        if prev_loc[0] > cur_loc[0]: #We komen van rechts
            return ([cur_loc[0],cur_loc[1]+1],cur_loc)
        return ([cur_loc[0]+1,cur_loc[1]],cur_loc)



def check_vertical(step_list):
    #we krijgen een lijst met wat er gebeurt op die regel
    row = np.zeros(140)
    special_char ='' #er is een bepaalde edge case waar ik rekening mee wil houden
    for step in sorted(step_list):
        
        
        if step[1] =='J':
            if special_char=='F': #we zien een j en hadden een f we zitten nog in de loop. Geen wijziging van status rechts
                #print('J in loop edge case')
                row[step[0]]=0
                continue
            elif special_char=='L':
                #print('J uit loop') #we zien een J maar er was geen F dus we zitten niet meer in de lopo
                row[step[0]+1:-1]=row[step[0]+1:-1]+1
            else:
                print('Jhjeeeelp')
        if step[1] =='7':
            if special_char=='L': #we zien een 7 en hadden een L hiervoor we zitten nog in de loop. Geen wijziging van status rechts
                row[step[0]]=0
                continue
            elif special_char=='F':
                #print('7 uit loop') #we zien een J maar er was geen L dus we zitten niet meer in de lopo
                row[step[0]+1:-1]=row[step[0]+1:-1]+1      
            else:
                print("7heeeellp")

        
        if step[1]=='L': #alles rechts hiervan verandert altijd van status
            row[step[0]+1:-1]=row[step[0]+1:-1]+1
            special_char='L' #voor de edge cases
            
        if step [1]=='F': #alles rechts hiervan verandert altijd van status
            row[step[0]+1:-1]=row[step[0]+1:-1]+1
            special_char='F' #voor de edge cases
            
        if step[1] == '|': #alles rechts hiervan verandert altijd van status
            row[step[0]+1:-1]=row[step[0]+1:-1]+1

        row[step[0]]=0 #De huidige plek is iig niet een leeg vak in de loop
        #print(step)
        #print(row)
        row=row%2 #maak van alles 2x in de loop 0x in de loop
    #print(row)
    return np.sum(row)
        
        
#loop door elke regel heen
#kijk hoeveel verticale er links zitten 
    
f = open("input_dag10.txt", "r")
opp= list()
for i,line in enumerate(f):
    line=line.replace('(','').replace(')','').replace('=','').replace('\n','').replace(',','')
    opp.append(line)
    
    for j,c in enumerate(line):
        if c=='S':
            i_start=i
            j_start=j


#doe iets met het gebied rond s om de next step te bepalen, nu handmatig gedaan
cur_loc=[0,0] #[x,y]
prev_loc=[0,0]
cur_loc[0]=j_start
cur_loc[1]=i_start

prev_loc[0]=cur_loc[0]-1 #Buis komt van links
prev_loc[1]=cur_loc[1]
token='7'

steps=0
step_list=list()
for i in range(140):
    step_list.append(list())

while not(cur_loc[0]==j_start and cur_loc[1]==i_start and steps>0):
    if opp[cur_loc[1]][cur_loc[0]]=='S':             
        (cur_loc,prev_loc)=next_step(token,cur_loc,prev_loc)
        steps=steps+1
    else:  
        (cur_loc,prev_loc)=next_step(opp[cur_loc[1]][cur_loc[0]],cur_loc,prev_loc)
        steps=steps+1
    #print(steps,opp[cur_loc[1]][cur_loc[0]], cur_loc,prev_loc)
    #Als het een vertiaak element is dan houden we hem bij.
    letter=opp[cur_loc[1]][cur_loc[0]]
    
    if letter!='S':
        step_list[cur_loc[1]].append([cur_loc[0],letter]) #y,x,letter
    else:
        step_list[cur_loc[1]].append([cur_loc[0],token]) 

area = 0
for i,line_info in enumerate(step_list):  
    line_area= check_vertical(line_info)
    #print(opp[i], line_area)
    area=area+line_area




print("Part 1:",int(steps/2))
print("Part 2",int(area))
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
