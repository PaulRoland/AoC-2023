# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 05:58:35 2023

@author: Paul
"""
import time
start_time = time.time_ns()

    
graph=dict()
f = open("input_dag25.txt", "r")

vert_V=list()
for line in f:
    cons = line.replace('\n','').split(':')
    con1=cons[0]
    if con1 not in vert_V:
        vert_V.append(con1)
    for con2 in cons[1][1:].split(' '):
        #Voeg verbindingen toe aan de graaf con1 -> con2 con2->con1
        if con2 not in vert_V:
            vert_V.append(con2)
            
        if con1 in graph:
            graph[con1].append([con2,1])
        else:
            graph.update({con1:[[con2,1]]})    
            
        if con2 in graph:
            graph[con2].append([con1,1])
        else:
            graph.update({con2:[[con1,1]]})   
f.close()


############
#Stoer Wagner
#Add the first options to the list and first scores
mincut=999
while len(vert_V)>1:
    #First fase min s t cut
    vert_A=list() #New set of vertices
    vert_A=[vert_V[0]] #Start randomly
    
    vertex_score=dict()
    vertex_ina=dict()
    #Start a dictionary off all vertices to keep track of the score
    for ver in vert_V:
        vertex_score.update({ver:0})
        vertex_ina.update({ver:0})
    
    #Add first vertex to inA
    vertex_ina[vert_A[0]]=1
    #Set the first scores of vertices
    vertex_score[vert_A[0]]=0
    
    for ver in graph[vert_A[0]]:
        vertex_score[ver[0]]=ver[1]
    
    while len(vert_A)!=len(vert_V):
        
        #Find the element with the heighest score
        v = list(vertex_score.values())
        k = list(vertex_score.keys())
        
        mostly_connected = k[v.index(max(v))]
        #print(len(vert_A),len(vert_V),mostly_connected,max(v))
        vert_A.append(mostly_connected) #add to A vertex list
        vertex_ina[mostly_connected]=1 #Add to in A
        
        #Add options and scores from the new vertex
        for ver in graph[mostly_connected]:
            if vertex_ina[ver[0]]==0: #Not already element of A #Faster than 'if elem in list'
                vertex_score[ver[0]]+=1
                
        for ver in vert_A:
            vertex_score[ver]=0


    ######
    #Merge last two vertices (s and t)
    vert1=vert_A[-2]
    vert2=vert_A[-1]
    new_edges1=dict()
    new_edges2=dict()
    new_edges_shared=dict()
    
    #Determine cut-size. Size of removing vert2
    cut=0
    for [ver,weight] in graph[vert2]:
        cut+=weight
        

    #Fix all new edges
    for [ver,weight] in graph[vert1]:
        if ver!=vert2:
            new_edges1.update({ver:weight})
                            
    for [ver,weight] in graph[vert2]:
        if ver!=vert1:
            new_edges2.update({ver:weight})
            
    #Remove connections to vert1
    for ver in new_edges1:
        graph[ver].remove([vert1,new_edges1[ver]])
    #Remove connections to ver2
    for ver in new_edges2:
        graph[ver].remove([vert2,new_edges2[ver]])
    
    #######
    #Update the graph with new information
    #Add connections to vert1+vert2
    #Forst find all the shared vertices and remove from the two lists
    for ver in list(new_edges1.keys()):
        if ver in new_edges2:
            #Combine weight in new edge
            new_edges_shared.update({ver:new_edges1[ver]+new_edges1[ver]})
            del new_edges1[ver]
            del new_edges2[ver]
    #Make one long list and add to the new vertex in graph a        
    new_edge_list=list()
    values=list(new_edges1.values())+list(new_edges2.values())+list(new_edges_shared.values())
    keys=list(new_edges1.keys())+list(new_edges2.keys())+list(new_edges_shared.keys())
    for [a,b] in zip(keys,values):
        new_edge_list.append([a,b])
    graph.update({(vert1+vert2):new_edge_list})
    
    #Add connections to the new node
    for [a,b] in zip(keys,values):
        graph[a].append([vert1+vert2,b])
    
    #remove the two vertices, as they are replaced by the shared
    del graph[vert1]
    del graph[vert2]
    
    #Haal oude vertex uit de lijsten en maak plaats voor de nieuwe
    vert_V.append((vert1+vert2))
    vert_V.remove(vert1)
    vert_V.remove(vert2)
    if cut<=mincut:
        print(len(vert_V),cut,vert2)
        cutvert=vert2
    mincut=min(mincut,cut)

print("Part 1",(1550-(len(cutvert)//3))*(len(cutvert)//3))
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
