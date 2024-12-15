# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 05:50:34 2023

@author: Paul
"""

import time
start_time = time.time_ns()
import numpy as np

def det_falling(brick_id): 
    n_falling=0
    i=0
    que=[brick_id]
    falling={brick_id}
    
    while i<len(que):
        #print(que)
        brick = que[i]
        #print(falling)
        #Kijk of de ondersteunende blokjes allemaal vallen, als een support niet aan het vallen is dan valt dit blokje ook niet
        brick_falling=True
        for support in brick_support_by[brick]:
            if support not in falling:
                brick_falling=False
        
        #Als hij valt (of het het eerste blokje is)
        if brick_falling==True or i==0:
            
            #Kijk welke steentjes op dit steentje steunen en voeg toe aan que
            z,x,y,L,B,H = bricks_stacked[brick]
            new_que = list(np.unique(stacked_volume[x:x+L,y:y+B,z+H]))

            #print(new_que)
            if 0 in new_que:
                new_que.remove(0)
            #print(brick_id,brick,new_que)            
            for item in new_que:
                que.append(item)
                    
            #Kijk of dit item al in de falling set zit, maar één keer laten vallen natuurlijk! Dit zorgt ook ervoor dat we het blokje zelf niet meetellen
            if brick in falling:
                n_falling-=1
                
            #Voeg dit item toe aan de falling set
            falling.add(brick)
            n_falling+=1  
        i+=1
    
    return n_falling
       
    
    
        

f = open("input_dag22.txt", "r")
bricks=list()
for i,line in enumerate(f):
    line=line.replace('(','').replace(')','').replace('=','').replace('\n','')
    
    brick_start,brick_end=line.split('~')
    x1,y1,z1 = brick_start.split(',')
    x2,y2,z2 = brick_end.split(',')   
    L=int(x2)-int(x1)+1
    B=int(y2)-int(y1)+1
    H=int(z2)-int(z1)+1
    bricks.append([int(z1),int(x1),int(y1),L,B,H,i+1])
f.close()

stack_surf=np.zeros([10,10])
sup_surf_id=np.zeros([10,10])
stacked_volume=np.zeros([10,10,200])
bricks_stacked=dict()
block_des=0
support_blocks=[]
single_load_blocks=[]
brick_support_by=dict()

for z1,x1,y1,L,B,H,brick_id in sorted(bricks):

    height = int(np.max(stack_surf[x1:x1+L,y1:y1+B]))  #Laagst beschikbare locatie
    
    #check supports
    support_list=[]
    for x in range(x1,x1+L):
        for y in range(y1,y1+B):
            if stack_surf[x,y]==height:
                support_list.append(sup_surf_id[x,y]) #Haal de baksteen ID uit support_surface

    if len(set(support_list))==1: #Als dit blok wordt ondersteund door exact een blok
         single_load_blocks.append(support_list[0]) #Dit blok mag sowieso niet weg   
    brick_support_by.update({brick_id:support_list})
    
    stack_surf[x1:x1+L,y1:y1+B]=height+H #Voeg dit blok toe aan de hoogte map   
    sup_surf_id[x1:x1+L,y1:y1+B]=brick_id #Voeg ID toe aan de hoogte map
    bricks_stacked.update({brick_id:[height+1,x1,y1,L,B,H]})
    stacked_volume[x1:(x1+L),y1:(y1+B),height+1:(height+1+H)]=brick_id
    
    
#Controleer voor elk blok of het blokken rechstreeks boven zicht heeft, hierbij helpt het aan de ondersteuning
#We hebben al een lijst van blokken die alleen een blok ondersteunen
support_blocks=list()
non_support_blocks=list()

for key,value in bricks_stacked.items():
    z,x,y,L,B,H = value
    if np.sum(stacked_volume[x:x+L,y:y+B,z+H])>0: #Tenminste een blokje steunt op dit blokje:
        support_blocks.append(key)
    else:
        non_support_blocks.append(key)
#Veilig disintegraten kan als het een non_support_block is of een support_block maar niet een single_load block
disint = set(non_support_blocks).union(set(support_blocks))-set(single_load_blocks)
print("Part 1",len(disint))

support_blocks=list()
non_support_blocks=list()

###Part 2 Kijk voor elke brick uit de single_load_blocks
total_falling=0
for block in list(set(single_load_blocks)-{0}):
    total_falling+=det_falling(block)
    #print(block, det_falling(block))

print("Part 2",total_falling)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
