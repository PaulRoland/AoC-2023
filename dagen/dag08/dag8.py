# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 05:58:50 2023

@author: Paul
"""

import time
start_time = time.time_ns()

import math

f = open("input_dag8.txt", "r")
hands=list()
sequence=f.readline().strip(' ').strip('\n')

node_dict ={}


list_a=list()
for i,line in enumerate(f):
    nodes = line.split(' ')
    if len(nodes)>1: 
        #add left
        node_dict.update({'L'+nodes[0].replace('\n',''):nodes[2].replace('(','').replace(',','').replace('\n','')})
        #add right
        node_dict.update({'R'+nodes[0].replace('\n',''):nodes[3].replace(')','').replace('\n','')})
        
        #Make a list of starting locations
        if nodes[0].replace('\n','')[2] == 'A':
            list_a.append(nodes[0].replace('\n',''))
f.close()

current_loc='AAA'
step_number=0
while current_loc !='ZZZ':
    current_instruction=sequence[step_number%len(sequence)]
    current_loc=node_dict[current_instruction+current_loc]
    step_number=step_number+1
print("Part 1:",step_number)

current_locations=list_a
loop_list=list()
for i,start_loc in enumerate(current_locations):
    step_number=0
    step_loop=0
    cur_loc= start_loc
    loc_loop='yippie'
    inloop = False
    while inloop == False:
        current_instruction=sequence[step_number%len(sequence)]
        cur_loc=node_dict[current_instruction+cur_loc]
        step_number=step_number+1
        step_loop=step_loop+1
        
        if cur_loc==loc_loop and step_loop==loop_length:
            #We zitten echt in een loop
            inloop = True
        
        if cur_loc[2]=='Z':
            loop_length=step_loop
            step_loop=0
            loc_loop=cur_loc
    loop_list.append(loop_length)

print("Part 2:", math.lcm(loop_list[0],loop_list[1],loop_list[2],loop_list[3],loop_list[4],loop_list[5]))
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
