# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 05:57:24 2023

@author: Paul
"""

import time
start_time = time.time_ns()

def change_xy(rocks):
    rock_list_yx= [[] for i in range(SIZE)]   
    for i,rock_list in enumerate(rocks):
        for rock in rock_list:
            rock_list_yx[rock[0]].append((i,rock[1]))
    return rock_list_yx

def tilt(rocks,direction):
    rock_min_list= [[] for i in range(SIZE)]   
    for j,column in enumerate(rocks):
        col_min=int((SIZE-1)*((direction-1)*-0.5))
        for rock in column[::direction]:
            if rock[1] == 0:
                #rock_min_list[j].append((rock[0],0))
                #Is de meeste logische manier om op te slaan,
                #Hierna willen we bijna altijd draaien, dus dat kan anders:
                rock_min_list[rock[0]].append((j,0))
                col_min=rock[0]+direction
            if rock[1]>0:
                #rock_min_list[j].append((col_min,rock[1]))
                #Is de meeste logische manier om op te slaan,
                #Hierna willen we bijna altijd draaien, dus dat kan anders:
                #Output is hiermee anders geindexed
                rock_min_list[col_min].append((j,rock[1]))
                col_min=col_min+direction
    return rock_min_list




f = open("input_dag14.txt", "r")
SIZE=100
row_min=[0]*SIZE
current_row=0
rock_list= [[] for i in range(SIZE)]
rock_number=1

for i,line in enumerate(f):
    line=line.replace('(','').replace(')','').replace('=','').replace('\n','')

    for j,c in enumerate(line):
        if c=='O': #Rock
            rock_list[j].append((i,1))
            rock_number+=1
            
        if c=='#':
            rock_list[j].append((i,0))

f.close()
n_rows=j+1

#Part 1:
rock_part1 = change_xy(tilt(rock_list,1))
total1=0
for column in rock_part1:
    for rock in column:
        #Sprint(rock)
        if rock[1]>0:
            total1+=n_rows-rock[0]

counter=0
configs=list()
looping = False
rocks=rock_list
while looping == False:
    rocks =  tilt(tilt(tilt(tilt(rocks,1),1),-1),-1)
    counter+=1
    
    if rocks in configs:
        for i,repeat in enumerate(configs):
            if repeat==rocks:
                loop_size=(counter)-(i+1)
                #print(counter,i,loop_size)
        configs.append(rocks)
        looping=True
    else:
        configs.append(rocks)

#Part 2:
#
rock_part2 = configs[(counter-loop_size-1 + (1000000000-counter)%loop_size)]

total2=0
for column in rock_part2:
    for rock in column:
        if rock[1]>0:     
            total2+=n_rows-rock[0]
print(total1)
print(total2)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))

    





