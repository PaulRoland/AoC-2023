# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 05:57:59 2023

@author: Paul
"""
import time
start_time = time.time_ns()
import math

f = open("input_dag20.txt", "r")

mem=dict()
net = dict()

for i,line in enumerate(f):
    line=line.replace('(','').replace(')','').replace('\n','')
    #print(line)
    data=line.split(' ')
    func =0
    key=data[0][1:]
    if data[0][0]=='%':
        func=1
    elif data[0][0]=='&':
        func=2
        mem.update({key:dict()})
            
    net_list = list()
    for item in data[2:]:
        net_list.append(item.replace(',',''))

    if func==0:
        key='broadcaster'

    net.update({key:[func,net_list,0]}) #Set state

f.close() 


#Make a list of memorys for the &s
for key,value in net.items():
    for dest in value[1]:
        if dest in mem:
            mem[dest].update({key:0})

pulses=[0,0]  #low,high pulses pulses[signal]=pulses[signal]+1

###Part 1
#
for j in range(1000):
    key_list=['broadcaster']
    sig_list=[0]
    src_list=['button']
    i=0
    
    while i<len(key_list):
        key=key_list[i]
        sig=sig_list[i]
        src=src_list[i]
        pulses[sig]=pulses[sig]+1
        
        if key not in net:
            #Deze is klaar of gaat buiten het net door met volgende signaaltje!
            i=i+1
            continue
        
        if net[key][0]==1 and sig==0: # Als het een flipflop is, en het signaal is laag
                state = (net[key][2]+1)%2 #flip the flopflop off>on, high pulse (1), on>off low pulse[0]
                net.update({key:[net[key][0],net[key][1],state]})  #update the state of the flopflip
                
                #Stuur een signaal naar alle connecties. voeg zetoe  aan de todo list
                for con in net[key][1]:  
                    key_list.append(con)
                    sig_list.append(state)
                    src_list.append(key)
                
        elif net[key][0]==2: # &
            #Update the signal
            mem[key].update({src:sig})
            
            mem_values=0
            
            ##Check of alle inputs 1 zijn van deze conjunction
            for slt,wrd in mem[key].items():
                mem_values+=wrd
            output=1
            if mem_values==len(mem[key]):
                output=0
             
            #Stuur een signaal naar alle connecties    
            for con in net[key][1]:  
                key_list.append(con)
                sig_list.append(output)
                src_list.append(key)             
    
                    
        elif net[key][0]==0: #broadcaster
            for con in net[key][1]:  #Stuur een laag signaal naar alle connecties
                key_list.append(con)
                sig_list.append(0)
                src_list.append(key)                
        i+=1
    
#####
#Part 2 kijk naar hoe lang elke boom is en welke waardes er teruggekoppeld worden door de conjunction modules
#Zoek degene die naar rx stuurt. RX krijgt data van conjunctions, deze conjunctions krijgen data van conjunctions
#Op papier de exacte methode gevonden om te kijken hoe snel een loop zichzelf herhaalt
#Welke stuurt naar RX
for key,waarde in net.items():
    if 'rx' in waarde[1]:
        end_key = key

#Welke conjunctions hangen hieraan
loop_keylist =list()
for key,waarde in mem[end_key].items():
    loop_keylist.append(key)

#Welke conjunctions hangen hier weer aan
loop_sources=list()
conj_dict=dict()
for key in loop_keylist:
    if key in mem:
        for sleutel,waarde in mem[key].items():
            loop_sources.append(sleutel)

#Bepaal wat de omslagperiode is van een bepaalde node en plaats ze bij de goede conjunction
for path in net['broadcaster'][1]:
    conj_sourc=dict()
    cur_key=path
    
    freq=2
    running=True
    while running:
        conj_sourc.update({cur_key:freq})
        freq=freq*2
        
        if len(net[cur_key][1])==1 and net[cur_key][1][0] in loop_sources:
            conj_dict.update({net[cur_key][1][0]:conj_sourc})
            break
        
        for options in net[cur_key][1]:
            if options not in loop_sources:
                cur_key=options
                break          
lcm_list = list()
#De conjunction stuurt een lage waarde uit ook terug naar nodes die hoog moeten zijn voor de
#conjunction zelf. De hoeveelheid button presses die je bespaart is dus de helft van de periode van die node.
for key,value in conj_dict.items():
    lcm_item=4096
    for slt in net[key][1]:
        if slt in value:
            lcm_item = lcm_item - (value[slt]/2)
    lcm_list.append(int(lcm_item))

     
print("Part 1:",pulses[0]*pulses[1])
print("Part 2:",math.lcm(*lcm_list))
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
