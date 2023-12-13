# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 05:48:15 2023

@author: Paul
"""
import time
start_time = time.time_ns()

def line_error(left,right):
    errors=0
    for (a,b) in zip(left,right):
        if a!=b:
            errors+=1
    
    return errors

def get_vertical_reflection(new_map,prev):
    vert_options=list()
    print('---------------')
    for row in new_map:
        print(row)
    #print(new_map)
    #Quick scan
    for i in range(len(new_map[0])-1):
        #print(i)
        if new_map[0][i]==new_map[0][i+1]:
            vert_options.append(i)
    print(vert_options)
    for option in vert_options:
        mirror_length = min(option+1,len(new_map[0])-option-1)
        
        mirror=True
        for row in new_map:
            #print("option",option)
            #print(row)
            #print(mirror_length)
            left = row[option+1-mirror_length:option+1]
            right = row[option+1:option+1+mirror_length]
            #print(left[::-1],right)
            print(option,row)
            if left[::-1]!=right:
                print("returning",option+1)
                mirror=False
                break
        #print("option",option,mirror)
        
        if mirror==True:
            if option+1 != prev:
                return option+1
    return 0  

def get_horizontal_reflection(normal_map,prev):
    #make new_map
    rotated_map=list()
    for j in range(len(normal_map[0])):
        string=''
        for i in range(len(normal_map)):
            string=string+normal_map[i][j]
        rotated_map.append(string)
    return get_vertical_reflection(rotated_map,prev)


def get_vertical_reflection_smudges(new_map):
    vert_options=list()
    #print(new_map)
    #Geen efficientie meer, gewoon kijken hoeveel fouten er zitten    
    for option in range(len(new_map[0])-1):
        mirror_length = min(option+1,len(new_map[0])-option-1)
        
        total_errors=0
        for nrow,row in enumerate(new_map):
            #print("option",option)
            #print(row)
            #print(mirror_length)
            left = row[option+1-mirror_length:option+1]
            right = row[option+1:option+1+mirror_length]
            #print(left[::-1],right)
            n_errors = line_error(left[::-1],right)
            total_errors +=n_errors
            
            if n_errors == 1:
                for nc,c in enumerate(left):
                    if c != right[-nc-1]: #Hier breekt de symmetry 
                        smudge_col=option+1-mirror_length+nc
                smudge_row=nrow
            
        #print("option",option,mirror)
        if total_errors==1:
            print("Smudge gevonden",option+1,smudge_row,smudge_col)
            return(smudge_row,smudge_col)
    return 0 

def get_horizontal_reflection_smudges(normal_map):
    #make new_map
    rotated_map=list()
    for j in range(len(normal_map[0])):
        string=''
        for i in range(len(normal_map)):
            string=string+normal_map[i][j]
        rotated_map.append(string)
    
    smudge_loc = get_vertical_reflection_smudges(rotated_map)
    
    if smudge_loc==0:
        return 0
    else:
        return (smudge_loc[1],smudge_loc[0])


f = open("input_dag13.txt", "r")
current_map=0
maps=list()
maps.append([])
for line in f:
    if line=='\n':

        current_map+=1
        maps.append([])
    else:
        line=line.replace('(','').replace(')','').replace('=','').replace('\n','')
        maps[current_map].append(line)
        
    #List of ints: groups = list(map(int,line.split(',')))
f.close()
total_score=0
total_score2=0
for n,new_map in enumerate(maps):
    ver=get_vertical_reflection(new_map,0) 
    hor=get_horizontal_reflection(new_map,0)
     
    score=hor*100+ver
    total_score += score
    
    print("map",n)

    #Find the smudge
    ver2=get_vertical_reflection_smudges(new_map)
    hor2=get_horizontal_reflection_smudges(new_map)
    #Get the location of the smudge
    if ver2==0:
        smudge_loc=hor2
    else:
        smudge_loc=ver2

    #Fix the smudge
    cleaned_map=new_map
    string=new_map[smudge_loc[0]]
    
    if string[smudge_loc[1]]=='#':
        string=string[:smudge_loc[1]]+'.'+string[smudge_loc[1]+1:]
    else:
       string=string[:smudge_loc[1]]+'#'+string[smudge_loc[1]+1:] 
       
    cleaned_map[smudge_loc[0]] = string
    
    for row in cleaned_map:
        print(row)
        
    #Analyze again
    ver3=get_vertical_reflection(new_map,ver) 
    hor3=get_horizontal_reflection(new_map,hor)  
    if ver2==0:
        score2=hor3*100
    else:
        score2=ver3
    print(score2)
    total_score2 += score2

    
print("Part 1",total_score)
print("Part 2",total_score2)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))