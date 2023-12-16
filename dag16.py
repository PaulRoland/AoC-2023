# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 05:58:13 2023

@author: Paul
"""
import time
import numpy as np
start_time = time.time_ns()


f = open("input_dag16.txt", "r")


def laser_move(loc,direction):
    #location is energized
    no_split=True
    new_direction=direction
    y=loc[0]
    x=loc[1]
    while no_split: #rechtdoor blijven gaan tot we een splitter tegenkomen
        y = y+new_direction[0]
        x = x+new_direction[1]
        
        #Check bounds
        if y<0 or x<0 or y>=len(surf) or x>=len(surf[0]):
            no_split=False
            return
        
        #energize current location
        energ[y][x]=1

        if surf[y][x]==1: # \ mirror
            new_direction=new_direction[::-1] #mirror switches x,y direction
                                      
        if surf[y][x]==2: # / mirror
            new_direction=new_direction[::-1] #mirror switches -x,-y direction
            new_direction[0]=-new_direction[0]
            new_direction[1]=-new_direction[1]

        if surf[y][x]==3:
            if new_direction[1] !=0: #We komen haaks op de splitter binnen
                #print("Splitter found",y,x, (y,x) in splitter_seen)
                no_split=False
                if (y,x) not in splitter_seen: #Kijk of we deze al gedaan hebben
                    #Branching
                    splitter_seen.append((y,x))
                    laser_move([y,x],[1,0])
                    laser_move([y,x],[-1,0])
                    
        if surf[y][x]==4:
            if new_direction[0] !=0: #We komen haaks op de splitter binnen
                #print("Splitter found",y,x, (y,x) in splitter_seen)
                no_split=False
                if (y,x) not in splitter_seen: #Kijk of we deze al gedaan hebben
                
                    #Branching
                    splitter_seen.append((y,x))
                    laser_move([y,x],[0,1])
                    laser_move([y,x],[0,-1])




splitter_seen=list()
energ = np.zeros((110,110))
surf = np.zeros((110,110))
for i,line in enumerate(f):
    line=line.replace('(','').replace(')','').replace('=','').replace('\n','')
    print(line)
    for j,c in enumerate(line):
        if c=='\\': #mirror 1
            surf[i][j]= 1
        if c=='/': #mirror 2
            surf[i][j]= 2
        if c=='|': #splitter 3
            surf[i][j]= 3
        if c=='-': #splitter 4
            surf[i][j]= 4 
        
f.close()
        
        
energ_list=list()
for i in range(len(surf)):
    print(i)
    laser_move([i,-1],[0,1]) #vanaf linkerkant
    energ_list.append(int(np.sum(energ)))
    energ = np.zeros((110,110))
    splitter_seen=[]
    

    laser_move([i,110],[0,-1]) #vanaf rechterkant
    energ_list.append(int(np.sum(energ)))
    energ = np.zeros((110,110))
    splitter_seen=[]
    
    laser_move([-1,i],[1,0]) #vanaf boven
    energ_list.append(int(np.sum(energ)))
    energ = np.zeros((110,110))
    splitter_seen=[]
    
    laser_move([110,i],[-1,0]) #vanaf boven
    energ_list.append(int(np.sum(energ)))
    energ = np.zeros((110,110))
    splitter_seen=[]
   
print(energ_list)   
print("Part 1", energ_list[0])
print("Part 2", max(energ_list))
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
