# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 05:58:13 2023

@author: Paul
"""
import time
import numpy as np
start_time = time.time_ns()


def laser_move(loc,direction):
    #location is energized 
    no_split=True
    new_direction=direction
    y=loc[0]
    x=loc[1]
    local_energy=np.zeros((SIZE,SIZE))
    
    while no_split: #rechtdoor blijven gaan tot we een splitter tegenkomen
        y = y+new_direction[0]
        x = x+new_direction[1]
        
        #Check bounds
        if y<0 or x<0 or y>=len(surf) or x>=len(surf[0]):
            no_split=False
            return local_energy
        
        #energize current location
        local_energy[y][x]=1

        if surf[y][x]==1: # \ mirror
            new_direction=new_direction[::-1] #mirror switches x,y direction
                                      
        if surf[y][x]==2: # / mirror
            new_direction=new_direction[::-1] #mirror switches -x,-y direction
            new_direction[0]=-new_direction[0]
            new_direction[1]=-new_direction[1]

        if surf[y][x]==3:
            if new_direction[1] !=0: #We komen haaks op de splitter binnen
                #print("Splitter found",y,x, (y,x) in splitter_seen)
                loaded_energy = splitter_energy_field[(y,x)]
                local_energy=local_energy + loaded_energy
                return local_energy
                  
        if surf[y][x]==4:
            if new_direction[0] !=0: #We komen haaks op de splitter binnen
                #print("Splitter found",y,x, (y,x) in splitter_seen)
                loaded_energy = splitter_energy_field[(y,x)]
                local_energy=local_energy + loaded_energy
                return local_energy
                    
    return local_energy


def splitter_energy(loc,direction): #Bekijkt welke splitters en oppervlakte een splitter bereikt.
    no_split=True
    new_direction=direction
    y=loc[0]
    x=loc[1]
    local_energy=np.zeros((SIZE,SIZE))
    
    splitter_seen=list()
    #Tak 1 van splitter
    while no_split: #rechtdoor blijven gaan tot we een splitter tegenkomen
        y = y+new_direction[0]
        x = x+new_direction[1]
        
        #Check bounds
        if y<0 or x<0 or y>=len(surf) or x>=len(surf[0]):
            break
        
        #energize current location
        local_energy[y][x]=1

        if surf[y][x]==1: # \ mirror
            new_direction=new_direction[::-1] #mirror switches x,y direction
                                      
        if surf[y][x]==2: # / mirror
            new_direction=new_direction[::-1] #mirror switches -x,-y direction
            new_direction[0]=-new_direction[0]
            new_direction[1]=-new_direction[1]

        if surf[y][x]==3:
            if new_direction[1] !=0: #We komen haaks op de splitter binnen
                if (y,x) not in splitter_seen: #Kijk of we deze al gedaan hebben
                    splitter_seen.append((y,x))
                break
            elif y == loc[0] and x==loc[1]: #Als we door de splitter zelf heen gaan zijn we ook klaar met een vertakking
                print('edge case?')
                break
                    
                    
        if surf[y][x]==4:
            if new_direction[0] !=0: #We komen haaks op de splitter binnen
                if (y,x) not in splitter_seen: #Kijk of we deze al gedaan hebben
                    splitter_seen.append((y,x))
                break
            elif y == loc[0] and x==loc[1]: #Als we door de splitter zelf heen gaan zijn we ook klaar met een vertakking
                print('edge case?')
                break
                
    #Tak 2
    y=loc[0]
    x=loc[1]
    new_direction=direction
    new_direction[0]=-new_direction[0]
    new_direction[1]=-new_direction[1]        
    while no_split: #rechtdoor blijven gaan tot we een splitter tegenkomen
        y = y+new_direction[0]
        x = x+new_direction[1]
        
        #Check bounds
        if y<0 or x<0 or y>=len(surf) or x>=len(surf[0]):
            break
        
        #energize current location
        local_energy[y][x]=1

        if surf[y][x]==1: # \ mirror
            new_direction=new_direction[::-1] #mirror switches x,y direction
                                      
        if surf[y][x]==2: # / mirror
            new_direction=new_direction[::-1] #mirror switches -x,-y direction
            new_direction[0]=-new_direction[0]
            new_direction[1]=-new_direction[1]

        if surf[y][x]==3:
            if new_direction[1] !=0: #We komen haaks op de splitter binnen
                if (y,x) not in splitter_seen: #Kijk of we deze al gedaan hebben
                    splitter_seen.append((y,x))
                break
            elif y == loc[0] and x==loc[1]: #Als we door de splitter zelf heen gaan zijn we ook klaar met een vertakking
                print('edge case?')
                break                    
        if surf[y][x]==4:
            if new_direction[0] !=0: #We komen haaks op de splitter binnen
                if (y,x) not in splitter_seen: #Kijk of we deze al gedaan hebben
                    splitter_seen.append((y,x))
                break
            elif y == loc[0] and x==loc[1]: #Als we door de splitter zelf heen gaan zijn we ook klaar met een vertakking
                print('edge case?')
                break        
    return local_energy,splitter_seen



def add_splitter(new_splitter,depth):
    #branching

    for splitter in splitter_details[new_splitter][1]: #details 1 heeft de nieuwe splitter
        if splitter not in splitter_seen:
            splitter_seen.append(splitter)
            add_splitter(splitter,depth+1)
    return


splitter_list=list()
f = open("input_dag16.txt", "r")
SIZE=110
surf = np.zeros((SIZE,SIZE))
for i,line in enumerate(f):
    line=line.replace('(','').replace(')','').replace('=','').replace('\n','')

    for j,c in enumerate(line):
        if c=='\\': #mirror 1
            surf[i][j]= 1
        if c=='/': #mirror 2
            surf[i][j]= 2
        if c=='|': #splitter 3
            surf[i][j]= 3
            splitter_list.append([i,j,1])
        if c=='-': #splitter 4
            surf[i][j]= 4 
            splitter_list.append([i,j,0])
f.close()

splitter_details = dict()
for splitter in splitter_list:
    if splitter[2]==0:
        (local_energy,splitters_seen) = splitter_energy([splitter[0],splitter[1]],[0,1])
        splitter_details.update({(splitter[0],splitter[1]):[local_energy,splitters_seen]})
    else:
        (local_energy,splitters_seen) = splitter_energy([splitter[0],splitter[1]],[1,0])
        splitter_details.update({(splitter[0],splitter[1]):[local_energy,splitters_seen]})

  
#Branch out all the splitter information
splitter_energy_field = dict()
for splitter in splitter_list:
    splitter_seen=[(splitter[0],splitter[1])]
    #Kijk of de splitter uitkomt bij een splitter
    for new_splitter in splitter_details[(splitter[0],splitter[1])][1]: #details 1 heeft de nieuwe splitter
        splitter_seen.append(new_splitter)
        add_splitter(new_splitter,0)
    
    
    #print(splitter_seen)
    loc_energy =np.zeros((SIZE,SIZE))
    for splitter_key in splitter_seen:
        loc_energy = loc_energy + splitter_details[splitter_key][0]
    
    splitter_energy_field.update({(splitter[0],splitter[1]):loc_energy})
    
    
energ_list=list()

for i in range(len(surf)):
    energy_field = laser_move([i,-1],[0,1]) #vanaf linkerkant
    energ_list.append(int(np.sum(energy_field>0)))
    energy_field = laser_move([i,SIZE],[0,-1]) #vanaf linkerkant
    energ_list.append(int(np.sum(energy_field>0)))
    energy_field = laser_move([-1,i],[1,0]) #vanaf linkerkant
    energ_list.append(int(np.sum(energy_field>0)))
    energy_field = laser_move([SIZE,i],[-1,0]) #vanaf linkerkant
    energ_list.append(int(np.sum(energy_field>0)))
  
print("Part 1", energ_list[0])
print("Part 2", max(energ_list))
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))