# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 05:50:34 2023

@author: Paul
"""

import time
start_time = time.time_ns()
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

class Brick:
    def __init__(self,x,y,z,L,B,H,ID):
        self.x=x
        self.y=y
        self.z=z
        self.L=L
        self.B=B
        self.H=H
        self.ID=ID
        self.zf=z
        self.nf=0
        self.supports=set()
        self.supported_by=set()
        
    def add_supported_by(self,ID):
        self.supported_by.add(ID)
        
    def add_supports(self,ID):
        self.supports.add(ID)
    
    def values(self):
        return self.x,self.y,self.z,self.L,self.B,self.H   
      
        
def det_falling(brick_id): 
    n_falling=0
    que=deque()
    
    #Voeg de eerste kandidaten toe aan de que
    for item in Bricks[brick_id].supports:
        que.append(item)
        
    falling={brick_id}
    
    while que:
        brick_id = que.popleft()
        
        #Kijk of de ondersteunende blokjes allemaal vallen, als een support niet aan het vallen is dan valt dit blokje ook niet
        brick_falling=True
        for support in Bricks[brick_id].supported_by:
            if support not in falling:
                brick_falling=False
        
        if brick_falling==True:
            
            #Kijk welke steentjes op dit steentje steunen en voeg toe aan que           
            for item in Bricks[brick_id].supports:
                que.append(item)
             
            #Kijk of dit item al in de falling set zit, maar één keer laten vallen natuurlijk!
            if brick_id in falling:
                continue
    
            #Voeg dit blokje toe aan de falling set
            falling.add(brick_id)
            Bricks[brick_id].nf=n_falling
            n_falling+=1  
    return n_falling
       

def can_disint():
    disint_zeker=set()
    disint_misschien=set()
    disint_niet=set()
    for ID,brick in Bricks.items():
        if len(brick.supports)==0: #dit blokje ondersteunt niets
            disint_zeker.add(ID)
        
        if len(brick.supported_by)==1:
            disint_niet.add(list(brick.supported_by)[0])
        
        if len(brick.supported_by)>1:
            for item in list(brick.supported_by):
                disint_misschien.add(item)
    return len(disint_zeker.union(disint_misschien)-disint_niet),list(disint_niet) #Stuur aantal en de lijst terug met single supports
    
        

f = open("input_dag22.txt", "r")
Bricks=dict()
Fall_order=list()
for i,line in enumerate(f):
    x,y,z,L,B,H=[int(x) for x in line.replace('~',',').replace('\n','').split(',')]
    Bricks.update({i+1:Brick(x,y,z,L-x+1,B-y+1,H-z+1,i+1)})
    Fall_order.append([z,i+1])
f.close()

#Stack the tower
surf_height=np.zeros([10,10])
surf_id=np.zeros([10,10])
bricks_stacked={}

for Z,ID in sorted(Fall_order):
    x,y,z,L,B,H = Bricks[ID].values()
    
    height = np.max(surf_height[x:x+L,y:y+B])  #Laagst beschikbare locatie
    
    #check supports
    for xx in range(x,x+L):
        for yy in range(y,y+B):
            if surf_height[xx,yy]==height and height!=0:
                Bricks[ID].add_supported_by(int(surf_id[xx,yy]))
                Bricks[int(surf_id[xx,yy])].add_supports(ID)

    surf_height[x:x+L,y:y+B]=height+H #Voeg dit blok toe aan de hoogte map   
    surf_id[x:x+L,y:y+B]=ID #Voeg ID toe aan de hoogte map
    Bricks[ID].z=height+1


total_p1,single_load_bricks = can_disint()

print("Part 1:",total_p1)
    
###Part 2 Kijk voor elke brick uit de single_load_blocks wat er gebeurt bij weghalen
total_falling=0
for ID in single_load_bricks:
    total_falling+=det_falling(ID)

print("Part 2",total_falling)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))


ax = plt.figure(figsize=(15,15)).add_subplot(projection='3d')
ax.set_box_aspect([1.0, 1.0, 20.0])
ax.set_axis_off()
color_list=[[1,0,0],[0,1,0],[0,0,1],[1,1,0],[0,1,1],[1,0,1]]

for ID,brick in Bricks.items():
    xx,yy,zz=np.indices((10,10,200))
    x,y,z,L,B,H = brick.values()
    shape = (xx >= x) & (yy >= y) & (zz >= z) &  (xx < x+L) & (yy < y+B) & (zz < z+H)
    color=color_list[ID%6]
    ax.voxels(shape,facecolors=color)
    print(ID)
plt.savefig('fig1.png',dpi=300)

