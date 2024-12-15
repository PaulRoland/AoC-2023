# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 05:58:35 2023

@author: Paul
"""
import time
import itertools as it
start_time = time.time_ns()

def kortstepad(node,end_node,total):
    global beste
    if total >= min(dist[node],beste):
        return
    
    if node==end_node:#einde  
        beste = total
    
    dist[node]=total
    
    #Open nieuwe vertakkingen
    for buur_node in graph[node]:
        kortstepad(buur_node,end_node,total+1)
    return
        

def check_connected(start_node):
    for new_node in graph[start_node]:
        if new_node not in nodes_visited:
            nodes_visited.update({new_node:1})
            check_connected(new_node)

graph=dict()
dist=dict()
f = open("input_dag25.txt", "r")
for i,line in enumerate(f):
    cons = line.replace('\n','').split(':')
    con1=cons[0]
    for con2 in cons[1][1:].split(' '):
        #Voeg verbindingen toe aan de graaf con1 -> con2 con2->con1
        if con1 in graph:
            graph[con1].append(con2)
        else:
            graph.update({con1:[con2]})    
            
        if con2 in graph:
            graph[con2].append(con1)
        else:
            graph.update({con2:[con1]})   
        
        #Losse dictionary voor het bijhouden van afstanden
        if con1 not in dist:
            dist.update({con1:1000000}) 
        if con2 not in dist:
            dist.update({con2:1000000})
f.close()
   
#Probeer in twee groepen te verdelen
#Begin bij een node, kijk naar de buren van de node.
#stel dat de rechtstreekse verbinding niet meer bestaat, wat is dan de kortste route?
#Maak hiermee een lijst van de impact van het verwijderen van elke losse verbinding
impactlijst=list()
nodes_gehad=list()

dist_inf = dist.copy()
punten_lijst=list(dist)

for con in punten_lijst:
    start_node=con  
    buur_nodes=list(graph[start_node])
    for node in buur_nodes:
        
        #Elk verbinding heeft twee startpunten dit is zonde van de tijd
        if [start_node,node] not in nodes_gehad:
            
            #Reset kortste pad
            beste=1000000
            dist = dist_inf.copy()
            
            #Verwijder de rechstreekse verbindingen
            graph[start_node].remove(node)
            
            #zoek het kortste pad zonder deze rechtstreekse verbinding
            kortstepad(start_node,node,0)
            
            #Voeg toe aan impactlijst
            impactlijst.append([beste,start_node,node])
            
            #Voeg verbiding weer toe aan graaf
            graph[start_node].append(node)            
            #Voeg nodes toe aan nodes_gehad zodat we geen dubbele berekening doen a->b b->a 
            nodes_gehad.append([start_node,node])
            nodes_gehad.append([node,start_node])
            
            
#We hebben nu een lijst met de impact van het verwijderen van elke losse verbinding
#Sorteer deze lijst op hoogste impact, brute force sets van 3 van deze verbindingen totdat de graaf nog maar bestaat uit 2 groepen
#Kans is zeer groot dat het drie van de n meest impactvolle verbindingen zijn
for remove3 in it.combinations(reversed(sorted(impactlijst)),3):
    nodes_visited=dict()
    
    #3 verbindingen uit de impactlijst
    rem1=remove3[0][1:]
    rem2=remove3[1][1:]
    rem3=remove3[2][1:]
    
    #Verwijder de drie verbindingen
    graph[rem1[0]].remove(rem1[1])
    graph[rem1[1]].remove(rem1[0])
    graph[rem2[0]].remove(rem2[1])
    graph[rem2[1]].remove(rem2[0])
    graph[rem3[0]].remove(rem3[1])
    graph[rem3[1]].remove(rem3[0])

    #Verwijder 6 verbindingen(3 heen terug) uit de graaf en kijk of hij connected is
    check_connected('qtf')
    
    #Voeg verwijderde verbindingen weer toe
    graph[rem1[0]].append(rem1[1])
    graph[rem1[1]].append(rem1[0])
    graph[rem2[0]].append(rem2[1])
    graph[rem2[1]].append(rem2[0])
    graph[rem3[0]].append(rem3[1])
    graph[rem3[1]].append(rem3[0])
    
    #Check connected maakt een dictionary van nodes. Kijk of dit evenveel items heeft als de hele graaf.
    if len(nodes_visited)==len(graph):
        continue
    else:
        print("Part 1:",len(nodes_visited)*(len(graph)-len(nodes_visited)))
        break

print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
