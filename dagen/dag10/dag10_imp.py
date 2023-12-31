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

def get_S_info(S_area,cur_loc):
    prev_loc=[0,0]
    j_start=cur_loc[0]
    i_start=cur_loc[1]
    x=cur_loc[0]
    y=cur_loc[1]
    S_up=False
    S_down=False
    S_left=False
    S_right=False

    if opp[y-1][x]=='|' or opp[y-1][x]=='7' or opp[y-1][x]=='F':
        S_up=True
        
    if opp[y+1][x]=='|' or opp[y+1][x]=='J' or opp[y+1][x]=='L':
        S_down=True
        
    if opp[y][x+1]=='-' or opp[y][x+1]=='J' or opp[y][x+1]=='7':
        S_right=True  
        
    if opp[y][x-1]=='-' or opp[y][x-1]=='L' or opp[y][x-1]=='F':
        S_left=True

    if S_left==True:
        if S_down==True:
            token='7'
        if S_up==True:
            token='J'
        if S_right==True:
            token='-'
        prev_loc[0]=j_start-1
        prev_loc[1]=i_start

    elif S_right==True:
        if S_down==True:
            token='F'
        if S_up==True:
            token='L'
        prev_loc[0]=j_start+1
        prev_loc[1]=i_start
    else:
        #S_left=False, S=right=False, enige optie is |
        token = '|'
        prev_loc[0]=j_start
        prev_loc[1]=i_start -1
        
    return (token,prev_loc)

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

def check_vertical(step_list,length):
    #we krijgen een lijst met wat er gebeurt op die regel
    row = np.zeros(length)
    special_char ='' #er is een bepaalde edge case waar ik rekening mee wil houden
    
    for step in sorted(step_list):
        row[step[0]]=0 #De huidige plek is iig een leeg vak in de loop
        
        if step[1] =='J':
            if special_char=='L': #we zien een j en hadden een f we zitten nog in de loop. Geen wijziging van status rechts
                #print('J uit loop') #we zien een J maar er was geen F dus we zitten niet meer in de lopo
                row[step[0]+1:-1]=row[step[0]+1:-1]+1
        if step[1] =='7':
            if special_char=='F':
                #print('7 uit loop') #we zien een J maar er was geen L dus we zitten niet meer in de lopo
                row[step[0]+1:-1]=row[step[0]+1:-1]+1      
      
        if step[1]=='L': #alles rechts hiervan verandert altijd van status
            row[step[0]+1:-1]=row[step[0]+1:-1]+1
            special_char='L' #voor de edge cases
            
        if step [1]=='F': #alles rechts hiervan verandert altijd van status
            row[step[0]+1:-1]=row[step[0]+1:-1]+1
            special_char='F' #voor de edge cases
            
        if step[1] == '|': #alles rechts hiervan verandert altijd van status
            row[step[0]+1:-1]=row[step[0]+1:-1]+1

    row=row%2 #maak van alles 2x in de loop 0x in de loop
    
    return (np.sum(row),row)
        
        
#loop door elke regel heen
#kijk hoeveel verticale er links zitten 
    
f = open("input_dag10.txt", "r")
opp= list()
for i,line in enumerate(f):
    line=line.replace('(','').replace(')','').replace('=','').replace('\n','').replace(',','')
    opp.append(line)
f.close()

#Bepaal startlocatie
for i,line in enumerate(opp):
    if 'S' in line:
        i_start=i
        j_start=line.index('S')
        break

#Bepaal hoe S vervangen kan worden en wat een bijbehorende prev_location is
cur_loc=[j_start,i_start]
(token,prev_loc)=get_S_info(opp,cur_loc)

opp[i_start]=opp[i_start].replace('S',token)

steps=0
step_list=list()
for i in range(len(opp)):
    step_list.append(list())

while not(cur_loc[0]==j_start and cur_loc[1]==i_start and steps>0):
    letter=opp[cur_loc[1]][cur_loc[0]]
    (cur_loc,prev_loc)=next_step(letter,cur_loc,prev_loc) 
    #print(steps,opp[cur_loc[1]][cur_loc[0]], cur_loc,prev_loc)
    #Als het een vertikaal element is dan houden we hem bij.
    letter=opp[cur_loc[1]][cur_loc[0]]
    step_list[cur_loc[1]].append([cur_loc[0],letter]) 
    steps=steps+1
    
area = 0
length= len(line)
for line_info in step_list:  
    (line_area,row)= check_vertical(line_info,length)
    area=area+line_area


print("Part 1:",int(steps/2))
print("Part 2",int(area))

print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))


for i,line_info in enumerate(step_list):
    (line_area,row)= check_vertical(line_info,length)
    string=''
    for c in row:
        string=string+str(int(c))
    string=string.replace('0','O').replace('1','I')
    for tube in line_info:
        string=string[:tube[0]]+tube[1]+string[tube[0]+1:]
    print(string)
print()
    

