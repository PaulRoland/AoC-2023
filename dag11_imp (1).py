# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 05:58:36 2023

@author: Paul
"""
import itertools as it

import time
start_time = time.time_ns()

def galaxy_dist(galaxy1,galaxy2):
    return [abs(galaxy1[0]-galaxy2[0])+abs(galaxy1[1]-galaxy2[1]),abs(galaxy1[2]-galaxy2[2])+abs(galaxy1[3]-galaxy2[3])]


#get list of galaxies
galaxy_list=list()
hor_list=list()
vert_list=list()


f = open("input_dag11.txt", "r")
y_exp=0
for i,line in enumerate(f):
    galaxy_inline=False
    
    for j,c in enumerate(line):
        if c=='#':
            galaxy_list.append([i,j,y_exp])
            hor_list.append(j)
            vert_list.append(i)
            galaxy_inline=True
    
    if galaxy_inline==False: #We zijn geen galaxies tegengekomen in deze lijn
        y_exp +=1
        
        
        
###
#Create list of horizontal expansion points
hor_options=range(j)
#locations of horizontal expansion, all options for x/y minus all x/y values that have a galaxy
hor_expansion=sorted(list(set(hor_options)-set(hor_list)))    


###
#expand the galaxy
###
time_factor=1000000-1
galaxy_list_expanded=list()
for i,galaxy in enumerate(galaxy_list):
    #Get the amount of horizontal expansions to this point
    n_x_exp = sum(1 for hor_point in hor_expansion if galaxy[1]>hor_point)
    #y expansion is already in galaxy[2] from initial append
    galaxy_list_expanded.append([galaxy[0]+galaxy[2],galaxy[1]+n_x_exp,galaxy[0]+galaxy[2]*time_factor,galaxy[1]+n_x_exp*time_factor])


###    
#Find total distances
total_distance1=0
total_distance2=0

#go through all unique pairs:
for galaxies in it.combinations(galaxy_list_expanded,2):
    galaxy1=galaxies[0]
    galaxy2=galaxies[1]    
    distance = galaxy_dist(galaxy1,galaxy2)
    total_distance1=total_distance1+distance[0]
    total_distance2=total_distance2+distance[1]
 
print("Part 1",total_distance1)
print("Part 2",total_distance2)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))