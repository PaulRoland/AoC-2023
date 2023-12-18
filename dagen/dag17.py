# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 05:59:09 2023

@author: Paul
"""
import time
import numpy as np
start_time = time.time_ns()


SIZE=141
beste=1e99
graph=list()

def maak_graaf(min_stappen,max_stappen):
    
    for row in range(SIZE):
        for col in range(SIZE):
            #Maak een graaf van alle gegevens. 
            #Je kan horizontaal dingen bereiken en verticaal dingen bereiken.
            #Twee list items per keer: (row*SIZE+col)*2 (row*SIZE+col)*2+1 is steeds de index
            graph.append([1e9,[]])
            graph.append([1e9,[]])
                         
                         
    for row in range(SIZE):
        for col in range(SIZE):
            
            #Index van graph is dan (row*SIZE+col), bijbehorende items zie hierboven
            gr_i = 2*(row*SIZE+col)
            #graph.append = [1e9,[]]  #Totale cost en lijst met horizontaal bereikbare buren
            #graph.append = [1e9,[]]  #Totale cost en lijst met vertikaal bereikbare buren
            
            for i in range(min_stappen,max_stappen+1):
                if col + i < SIZE: #Loop naar rechts
                    cost = np.sum(grid[row,col+1:col+i+1])
                    graph[gr_i][1].extend([(row*SIZE+col+i)*2+1,cost]) #even verbind met oneven voor hor/ver afwisseling
                    
                if col - i >= 0: #Loop naar links
                    cost = np.sum(grid[row,col-i:col])
                    graph[gr_i][1].extend([(row*SIZE+col-i)*2+1,cost])
                    
                if row + i < SIZE: #Loop naar beneden
                    cost = np.sum(grid[row+1:row+i+1,col])
                    graph[gr_i+1][1].extend([((row+i)*SIZE+col)*2,cost]) #oneven verbind met even voor ver/hor afwisseling    
                             
                if row - i >= 0: #Loop omhoog
                    cost = np.sum(grid[row-i:row,col])
                    graph[gr_i+1][1].extend([((row-i)*SIZE+col)*2,cost])                 

            #We hebben nu een volledige graaf gemaakt van het probleem   
    

def graph_crawl(nbrs,total):
    global beste
    if total >= min(graph[nbrs][0],beste):
        return #Totaal is nu al te hoog, dit is geen oplossing
    
    if nbrs == 2*SIZE*SIZE-1 or nbrs == 2*SIZE*SIZE-2:  #einde
        print("Beste tot nu toe!",total)    
        beste = total
    
    graph[nbrs][0]=total
    
    #pareltje om de neighbours en de bijbehorende pad lengtes te vinden
    #Open nieuwe vertakkingen
    for nbrs,path_cost in zip(graph[nbrs][1][::2],graph[nbrs][1][1::2]):
        graph_crawl(nbrs,total+path_cost)
    
    return


f = open("input_dag17.txt", "r")

grid = np.zeros((SIZE,SIZE))
for i,line in enumerate(f):
    line=line.replace('(','').replace(')','').replace('=','').replace('\n','')
    for j,c in enumerate(line):
        grid[i][j]=int(c)
f.close()

maak_graaf(1,3)
beste=1e99
#Oplossen met traag kortste pad algoritme. Blijft vertakken tot je langer bent, of schrijf de kortere waarde weg
#pareltje om de neighbours van plekje 1 en de bijbehorende pad lengtes te vinden
for nbrs,path_cost in zip(graph[0][1][::2]+graph[1][1][::2],graph[0][1][1::2]+graph[1][1][1::2]):
    print(nbrs,path_cost)
    graph_crawl(nbrs,path_cost) 
beste_p1=beste

#reset de boel

graph=list()
maak_graaf(4,10)
beste=1e99
#pareltje om de neighbours van plekje 1 en de bijbehorende pad lengtes te vinden
for nbrs,path_cost in zip(graph[0][1][::2]+graph[1][1][::2],graph[0][1][1::2]+graph[1][1][1::2]):
    print(nbrs,path_cost)
    graph_crawl(nbrs,path_cost) 
beste_p2=beste



print("Part 1:",beste_p1)
print("Part 2:",beste_p2)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))