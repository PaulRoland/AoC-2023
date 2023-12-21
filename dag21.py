# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 05:57:08 2023

@author: Paul
"""

import time
start_time = time.time_ns()
import math
import numpy as np
f = open("input_dag21.txt", "r")

SIZE=131
grid=np.zeros([SIZE,SIZE])
for y,line in enumerate(f):
    for x,c in enumerate(line):
        if c=='#':
            grid[y,x]=1
        if c=='S':
            start_x=x
            start_y=y
f.close()


'''
max_steps=64
nsteps=0
steps =[[start_x,start_y]]

visited=[[],[]]

while nsteps<max_steps:
    nsteps+=1
    #We kunnen naar links, rechts, boven en onder
    new_steps=list()
    #print(steps)
    for x,y in steps:
        #rechts 
  
        if x+1<SIZE:
            if grid[y,x+1]==0 and [x+1,y] not in visited[(nsteps)%2]:
                visited[(nsteps)%2].append([x+1,y])    
                new_steps.append([x+1,y])
        #links
        if x-1>=0:
            if grid[y,x-1]==0 and [x-1,y] not in visited[(nsteps)%2]:
                visited[(nsteps)%2].append([x-1,y])    
                new_steps.append([x-1,y])
        #onder
        if y+1<SIZE:
            if grid[y+1,x]==0 and [x,y+1] not in visited[(nsteps)%2]:
                visited[(nsteps)%2].append([x,y+1])    
                new_steps.append([x,y+1])       
        #boven
        if y-1>=0:
            if grid[y-1,x]==0 and [x,y-1] not in visited[(nsteps)%2]:
                visited[(nsteps)%2].append([x,y-1])    
                new_steps.append([x,y-1])
    
    steps=new_steps
    if nsteps==64:
        print("Part 1:",len(visited[0]))
'''
#Dit algoritme werkt niet voor elke input. De input is zo gemaakt dat je altijd in 131 bij het volgende
#punt kan komen. Daardoor is er een bepaalde bereikbaarheid van vlakken op te maken (zie plaatje)
#We hebben een aantal oneven vlakken, een aantal even vlakken en we hebben een rand waar we rekening mee moeten houden.
#Ook is de rest van de modulo SIZE: 65 hierdoor komen we in een makkelijker scenario (zie plaatje)
'''
nsteps=0
steps =[[start_x,start_y]]
visited=[[],[]]
max_steps=2*SIZE+65

while nsteps<max_steps:
    nsteps+=1
    #We kunnen naar links, rechts, boven en onder
    new_steps=list()
    #print(steps)
    for x,y in steps:
        #rechts 
        if grid[y%SIZE,(x+1)%SIZE]==0 and [x+1,y] not in visited[(nsteps)%2]:
            visited[(nsteps)%2].append([x+1,y])    
            new_steps.append([x+1,y])
            #links

        if grid[y%SIZE,(x-1)%SIZE]==0 and [x-1,y] not in visited[(nsteps)%2]:
            visited[(nsteps)%2].append([x-1,y])    
            new_steps.append([x-1,y])
            #onder

        if grid[(y+1)%SIZE,x%SIZE]==0 and [x,y+1] not in visited[(nsteps)%2]:
            visited[(nsteps)%2].append([x,y+1])    
            new_steps.append([x,y+1])       
            #boven
        if grid[(y-1)%SIZE,x%SIZE]==0 and [x,y-1] not in visited[(nsteps)%2]:
            visited[(nsteps)%2].append([x,y-1])    
            new_steps.append([x,y-1])
    steps=new_steps

max_steps=26501365
N=int(math.floor(max_steps/SIZE))

aantal_oneven = N*N
aantal_even = (N+1)*(N+1)
aantal_vijfhoeken= N-1
aantal_punten=1
aantal_driehoeken = N

driehoeken_even =0
driehoeken_oneven=0

for x,y in visited_even:
    if abs(x-65)+abs(y-65) > 65:
        driehoeken_even+=1

for x,y in visited_oneven:
    if abs(x-65)+abs(y-65) > 65:
        driehoeken_oneven+=1


#De vier puntjes en vier vijfhoeken zijn allemaal even
#Eerst geprobeerd op de andere methode uit het plaatje
A=B=C=D=E=F=G=H=I=J=K=L=0
VLK1=VLK2=VLK3=VLK4=VLK5=0

for x,y in visited[0]:
    #Puntjes
    if x>=0 and x<SIZE and y>=2*SIZE:
        C+=1
    elif x>=0 and x<SIZE and y<-SIZE:
        A+=1
    elif y>=0 and y<SIZE and x>=2*SIZE:
        B+=1
    elif y>=0 and y<SIZE and x<-SIZE:
        D+=1
        
    #Vijfhoeken
    elif y>=SIZE and y<2*SIZE and x<0 and x>=-SIZE:
        H+=1
    elif y>=SIZE and y<2*SIZE and x>=SIZE and x<2*SIZE:
        G+=1        
    elif y<0 and y>=-SIZE and x>=SIZE and x<2*SIZE:
        F+=1
    elif y<0 and y>=-SIZE and x<0 and x>=-SIZE:
        E+=1
    #Driehoekjes
    elif x>=SIZE and y<-SIZE:
        J+=1
    elif x<-SIZE and y<0:
        I+=1
    elif x>=SIZE and y>=2*SIZE:
        K+=1
    elif x<0 and y>=2*SIZE:
        L+=1
    #volvlak

#De kleine witte driehoekjes zijn trouwens wel oneven
for x,y in visited[0]:
    #Driehoekjes
    if x>=SIZE and y<-SIZE:
        J+=1
    if x<-SIZE and y<0:
        I+=1
    if x>=SIZE and y>=2*SIZE:
        K+=1
    if x<0 and y>=2*SIZE:
        L+=1        




totaal_p2=aantal_oneven*vlak_oneven
totaal_p2+=aantal_even*vlak_even
totaal_p2+=aantal_vijfhoeken*(E+F+G+H)
totaal_p2+=aantal_driehoeken*(I+J+K+L)
totaal_p2+=aantal_punten*(A+B+C+D)
print("Part 2:",totaal_p2)
'''

#Na uren kutten en vier foute antwoorden ga ik toch gewoon voor het fitten van de polynoom ax**2+bx+c die in bovenstaande berekening ook zit.
# N*N*even, (N-1) * (n-1) oneven etc Geeft N^2a+Nb+c= aantal. Voor een tweede orde polynoom hebben we drie datapunten nodig.
#Beetje jammer maargoed, ik denk dat ik er niet heel ver weg van zit, later nog maar eens proberen op de mooiere methode.
####
#Van het uitschrijven van de berekening weet ik wel dat de term voor de N2 gelijk is aan de even en de oneven waarde van de vlakken.
#Hiervoor heb ik nog maar 2 punten nodig om het 2e orde polynoom toch te fitten.
#Onderstaande zou vast ook nog wat sneller moeten kunnen, maar eens wat meer in dit soort algoritmes verdiepen.

nsteps=0
steps =[[start_x,start_y]]
visited=[[],[]]
max_steps=SIZE+65
fit_data=list()
even_vlak=0
oneven_vlak=0
while nsteps<max_steps:
    nsteps+=1
    #We kunnen naar links, rechts, boven en onder
    new_steps=list()
    #print(steps)
    for x,y in steps:
        #rechts 
        if grid[y%SIZE,(x+1)%SIZE]==0 and [x+1,y] not in visited[(nsteps)%2]:
            visited[(nsteps)%2].append([x+1,y])    
            new_steps.append([x+1,y])
            #links

        if grid[y%SIZE,(x-1)%SIZE]==0 and [x-1,y] not in visited[(nsteps)%2]:
            visited[(nsteps)%2].append([x-1,y])    
            new_steps.append([x-1,y])
            #onder

        if grid[(y+1)%SIZE,x%SIZE]==0 and [x,y+1] not in visited[(nsteps)%2]:
            visited[(nsteps)%2].append([x,y+1])    
            new_steps.append([x,y+1])       
            #boven
        if grid[(y-1)%SIZE,x%SIZE]==0 and [x,y-1] not in visited[(nsteps)%2]:
            visited[(nsteps)%2].append([x,y-1])    
            new_steps.append([x,y-1])
    steps=new_steps
    if nsteps==64:
        print("Part 1:",len(visited[0]))
    if nsteps%SIZE==65:
        fit_data.append(len(visited[nsteps%2]))
    if nsteps==142:
        for x,y in visited[0]:
            if x>=0 and x<SIZE and y>=0 and y<SIZE:
                even_vlak+=1
    if nsteps==143:
        for x,y in visited[1]:
            if x>=0 and x<SIZE and y>=0 and y<SIZE:
                oneven_vlak+=1

#Fit ax^2 + bx+ c met de datapunten        
#Van het uitschreven weten we dat de term voor N^2 gelijk is aan het constante evenvlak+onevenvlak, dat scheelt een datapunt en dus veel rekenen
x_data=[0,1]
a = even_vlak + oneven_vlak

b = (fit_data[0]-fit_data[1])/(x_data[0]-x_data[1])-a*(x_data[0]+x_data[1])
c = fit_data[1]-a*x_data[1]**2-b*x_data[1]

N=math.floor(26501365/SIZE)
totaal_p2 = a*N**2+b*N+c

print("Part 2",round(totaal_p2))


print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))