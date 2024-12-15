# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 07:44:59 2023

@author: Paul
"""
import numpy as np
import time
start_time = time.time_ns()
from collections import deque
SIZE=141
grid=np.zeros((141,141))

grid_dict={'#':5,'.':0,'>':1,'<':2,'^':3,'v':4}

f = open('input_dag23.txt','r')
for y,line in enumerate(f):
    line=line.replace('\n','')
    for x,c in enumerate(line):
        grid[y,x]=grid_dict[c]
f.close()

def get_slopedir(prev_loc,cur_loc,slope_id):
    #print(prev_loc,cur_loc,slope_id)
    if slope_id==1: # >
        if prev_loc[1]<cur_loc[1]:
            return 1
        else:
            return -1
    if slope_id==2: # <
        if prev_loc[1]>cur_loc[1]:
            return 1
        else:
            return -1
    if slope_id==3: # ^
        if prev_loc[0]>cur_loc[0]:
            return 1
        else:
            return -1
    if slope_id==4: # v
        if prev_loc[0]<cur_loc[0]:
            return 1
        else:
            return -1

def graph_add_nodes(start_node,end_node,path_length,slope_dir):
    #print(start_node,end_node,path_length,slope_dir)
    if slope_dir>=0:
        #Voeg verbinding in graaf toe in een bepaalde richting
        #print('Adding node',start_node,'->',end_node,path_length,slope_dir)
        if start_node in graph:
            if [end_node,path_length] not in graph[start_node][1]:
                graph[start_node][1].append([end_node,path_length])
        else:
            graph.update({start_node:[0,[[end_node,path_length]]]})
    
    if slope_dir<=0  : 
        #Voeg verbinding in graaf toe in de andere richting
        #print('Adding node',end_node,'->',start_node,path_length,slope_dir)
        if end_node in graph:
            if [start_node,path_length] not in graph[end_node][1]:
                graph[end_node][1].append([start_node,path_length])
        else:
            graph.update({end_node:[0,[[start_node,path_length]]]})


    #Onafhankelijk van de slopedir maken we ook een connected graph voor p2
    if start_node in graph_connected:
        if [end_node,path_length] not in graph_connected[start_node][1]:
            graph_connected[start_node][1].append([end_node,path_length])
    else:
        graph_connected.update({start_node:[0,[[end_node,path_length]]]})
        
    if end_node in graph_connected:
        if [start_node,path_length] not in graph_connected[end_node][1]:
            graph_connected[end_node][1].append([start_node,path_length])
    else:
        graph_connected.update({end_node:[0,[[start_node,path_length]]]})        
    


def langste_pad(node,total,end_node,visited_list):
    
    if total > graph[node][0]:
        graph[node][0]=total #langste pad mogelijk om hier te komen
    
    if node==end_node:
        return
    
    #Open nieuwe vertakkingen, kijk of we niet al op de nieuwe node zijn geweest, want dan gaat het anders lang duren
    for new_node,path_length in graph[node][1]:
        if new_node not in visited_list:
            new_visited = list(visited_list) #Rare python list memory geheugen shit
            new_visited.append(new_node)
            langste_pad(new_node,total+path_length,end_node,new_visited)


def langste_pad_connected(node,total,end_node,visited_list):
    global langste_pad_gevonden
    #print(node,visited_list)
    if node==end_node:
        if total> graph_connected[node][0]:
            langste_pad_gevonden=list(visited_list)
    
    if total > graph_connected[node][0]:
        graph_connected[node][0]=total #langste pad mogelijk om hier te komen
    
    if node==end_node:
        return
    
    #Open nieuwe vertakkingen, kijk of we niet al op de nieuwe node zijn geweest, want dan gaat het anders lang duren
    for new_node,path_length in graph_connected[node][1]:
        if new_node not in visited_list:
            new_visited = list(visited_list) #Rare python list memory geheugen shit
            new_visited.append(new_node)
            langste_pad_connected(new_node,total+path_length,end_node,new_visited)



map_start=[0,1,-1,1] #y,x,prev_y,prev_x
map_end=[SIZE-1,SIZE-2]
nodes_visited={}
graph={}
graph_connected={}

que=deque()
que.append(map_start)

steps=[[0,1],[0,-1],[-1,0],[1,0]]

while que:
    start_y,start_x,prev_y,prev_x = que.popleft()
    start_node = str(start_y)+','+str(start_x)

    #We zijn de laatste node aan het evalueren, dat is niet nodig
    if start_y==map_end[0] and start_x == map_end[1]:
        continue
    
    
    # Kijk in welke richting we allemaal kunnen lopen
    for step1 in steps:
        if start_y+step1[0]==prev_y and start_x+step1[1]==prev_x:
            continue #Ga door met een andere step dan deze, deze richting is al ontdekt
        
        if grid[start_y+step1[0],start_x+step1[1]]==5:
            continue #Dit is geen vakje waar we op kunnen staan 
    
        if start_y+step1[0]<0:
            continue #We gaan van de kaart
            
              
        prev_loc=[start_y,start_x]
        cur_loc=[start_y+step1[0],start_x+step1[1]]
        path_length=1
        slope_dir=0 #Pad kan: 0 beide kanten op, 1 met de huidige richting mee, -1 tegen de huidige richting in.
       
       ########################## 
       #Loop tot je een punt met vertakkingen tegenkomt of bij het einde bent
        while True:
            #print(cur_loc)
            if cur_loc==map_end:
                break
            
            if grid[cur_loc[0],cur_loc[1]]>0: #Als we op een slope staan
                slope_dir = get_slopedir(prev_loc,cur_loc,grid[cur_loc[0],cur_loc[1]])
                #print(start_node,slope_dir)
            
            n_options=0
            for step in steps:
                if grid[cur_loc[0]+step[0],cur_loc[1]+step[1]] < 5 and [cur_loc[0]+step[0],cur_loc[1]+step[1]]!=prev_loc:
                    step_option=step
                    n_options+=1
            
            if n_options>1:
                #We zijn bij een vertakking
                break
            
            prev_loc=cur_loc
            cur_loc=[cur_loc[0]+step_option[0],cur_loc[1]+step_option[1]]
            path_length+=1
        
        
        ##################
        #Klaar met lopen in een richting, voeg de nodes toe aan de graph  
        end_node=str(cur_loc[0])+','+str(cur_loc[1])
        
        graph_add_nodes(start_node,end_node,path_length,slope_dir)
        
        #Voeg nieuwe ontdekkingsmogelijkheden 1x toe aan de que
        if end_node not in nodes_visited:
            nodes_visited.update({end_node:[cur_loc[0],cur_loc[1]]})
            que.append([cur_loc[0],cur_loc[1],prev_loc[0],prev_loc[1]])



start_node = str(map_start[0])+','+str(map_start[1])
end_node=str(map_end[0])+','+str(map_end[1])
graph.update({end_node:[0,[]]})
print("G(r)aaf gemaakt!")

langste_pad(start_node,0,end_node,[start_node])
print("Part 1:",graph[end_node][0])

langste_pad_connected(start_node,0,end_node,[start_node])
print("Part 2:",graph_connected[end_node][0])
#Langste pad algoritme
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
        
    
