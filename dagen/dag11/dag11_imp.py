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
for i,line in enumerate(f):
    for j,c in enumerate(line):
        if c=='#':
            galaxy_list.append([i,j])
            hor_list.append(j)
            vert_list.append(i)

###
#Create list of expansion points
###
hor_options=range(j)
vert_options=range(i)

#locations of horizontal expansion, all options for x/y minus all x/y values that have a galaxy
hor_expansion=sorted(list(set(hor_options)-set(hor_list)))    
vert_expansion=sorted(list(set(vert_options)-set(vert_list)))

###
#expand the galaxy
###
time_factor=1000000-1
galaxy_list_expanded=list()
n_y_exp=0
y_len=len(vert_expansion)
for i,galaxy in enumerate(galaxy_list):
    #Get the amount of horizontal expansions to this point
    n_x_exp = sum(1 for hor_point in hor_expansion if galaxy[1]>hor_point)
    #n_y_exp = sum(1 for vert_point in ver_expansion if galaxy[0]>vert_point)
    #Y is sorted so we can keep track without iterating the forloop
    if n_y_exp<y_len:
        if galaxy[0]>vert_expansion[n_y_exp]:
            n_y_exp=n_y_exp+1
        
    galaxy_list_expanded.append([galaxy[0]+n_y_exp,galaxy[1]+n_x_exp,galaxy[0]+n_y_exp*time_factor,galaxy[1]+n_x_exp*time_factor])
    

#total distances
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
