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
sequence=f.readline().replace('(','').replace(')','').replace('=','').replace('\n','').replace(',','')
seq_len=len(sequence)
node_dict ={}
node_list = list()
starter_list=list()
for i,line in enumerate(f):
    nodes = line.replace('(','').replace(')','').replace('=','').replace('\n','').replace(',','').split(" ")
    if len(nodes)>1: 
        #Beide entries toevoegen aan dictionary met tuple notation: 8 microseconde sneller in totaal dan twee keer los wat toevoegen
        node_dict.update([('L'+nodes[0],nodes[2]),('R'+nodes[0],nodes[3])])
        node_list.append(nodes[0])
        #add left
        #node_dict.update({'L'+nodes[0]:nodes[2]})
        #key wordt bijv LAAA, waarde BBB
        #add right
        #node_dict.update({'R'+nodes[0]:nodes[3]})

        #Make a list of starting locations
        if nodes[0][2] == 'A':
            starter_list.append(nodes[0])
            if nodes[0]=='AAA':
                aaa_loc=len(starter_list)
f.close()

#De sequenced herhaalt elke 283 stappen, je kan dus bepalen waar elke locatie
#naartoe gaat in 283 stappen en daar een dictionary van maken, misschien gaat
#de volgende stap dan sneller

node_dict_283={}
for start in node_list:
    cur_loc=start
    for i in range(seq_len):
        current_instruction=sequence[i%seq_len]
        cur_loc=node_dict[current_instruction+cur_loc]
    node_dict_283.update({start:cur_loc})


current_locations=starter_list
loop_list=list()
for i,start_loc in enumerate(current_locations):
    step_number=0
    cur_loc= start_loc
    loc_loop='yippie'
    inloop = False
    while inloop == False:
        current_instruction=sequence[step_number%seq_len]
        cur_loc=node_dict_283[cur_loc]
        step_number=step_number+1
        
        if cur_loc[2]=='Z':
            inloop = True
    loop_list.append(step_number)
    
print("Part 1:",283*loop_list[aaa_loc-1])
print("Part 2:",283*math.lcm(loop_list[0],loop_list[1],loop_list[2],loop_list[3],loop_list[4],loop_list[5]))
#Nee dit is uiteindelijk niet sneller dan dag8_imp.py
#Het bepalen van de mapping van elke node duurt langer dan de methode waar je rechtstreeks de loop lengte bepaalt
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))