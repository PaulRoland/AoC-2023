# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 05:59:17 2023

@author: Paul
"""
import time
start_time = time.time_ns()

seed_soil = list()
soil_fert = list()
fert_water= list()
water_light=list()
light_temp=list()
temp_hum=list()
hum_loc=list()

cur_map=-1

def get_number_list(lst):
    new_lst = [int(x) for x in lst]
    return new_lst

def get_mapping(source,mapping):
    for value in mapping:
        #value[0] is the destination start of the mapping
        #value[1] is the source start of the mapping
        #value[2] is the range of the mapping
    
        if source>=value[1] and source<value[1]+value[2]:
            #Hoe ver zijn we in de mappinglijst
            return value[0]-value[1]+source
    return source

def get_reverse_mapping(destination,mapping):
    for value in mapping:
        #value[0] is the destination start of the mapping
        #value[1] is the source start of the mapping
        #value[2] is the range of the mapping
    
        if destination>=value[0] and destination<value[0]+value[2]:
            #Hoe ver zijn we in de mappinglijst
            return value[1]-value[0]+destination
    return destination

def check_seed(seed,seed_list):
    #print(seed,seed_list)
    for i,seed_start in enumerate(seed_list):
        if i%2==0:
            if seed>=seed_start and seed<seed_start+seed_list[i+1]:
                return True
    return False

f = open("input_dag5.txt", "r")
for i,line in enumerate(f):
    if i==0:
        seed_list = get_number_list(line.split()[1:])
    else:
        #We laden 7 verschillende maps
        if '-to-' in line: # We beginnen aan een nieuw mapping
            cur_map=cur_map+1
            continue
        if ' ' not in line:
            continue
        if cur_map == 0:
            seed_soil.append(get_number_list(line.split()))
        if cur_map == 1:
            soil_fert.append(get_number_list(line.split()))
        if cur_map == 2:
            fert_water.append(get_number_list(line.split()))
        if cur_map == 3:
            water_light.append(get_number_list(line.split()))
        if cur_map == 4:
            light_temp.append(get_number_list(line.split()))
        if cur_map == 5:
            temp_hum.append(get_number_list(line.split()))  
        if cur_map == 6:
            hum_loc.append(get_number_list(line.split()))
                          
f.close()
#Lijst van zaden en lijst van verschillende mappings
loc_list=list()
for seed in seed_list:
    soil = get_mapping(seed,seed_soil)
    fert = get_mapping(soil,soil_fert)
    water= get_mapping(fert,fert_water)
    light= get_mapping(water,water_light)
    temp = get_mapping(light,light_temp)
    hum  = get_mapping(temp,temp_hum)
    loc  = get_mapping(hum,hum_loc)
    
    loc_list.append(loc)
print("Part 1:",min(loc_list))

#Locaties bruteforcen totdat er een zaad is wat in de lijst staat.
#Locatie>zaden bruteforce leek me sneller dan alle zaden doorrekenen en dan de laagste locatie nemen.
loc = 0
loc_gev =0
while loc_gev == 0:
    hum  = get_reverse_mapping(loc,hum_loc)
    temp = get_reverse_mapping(hum,temp_hum)
    light= get_reverse_mapping(temp,light_temp)
    water= get_reverse_mapping(light,water_light)
    fert = get_reverse_mapping(water,fert_water)
    soil = get_reverse_mapping(fert,soil_fert)
    seed = get_reverse_mapping(soil,seed_soil)
    
    #print(seed,soil,fert,water,light,temp,hum,loc)
    if(check_seed(seed,seed_list)):
        #De eerste hit is ook meteen de laagste locatie, dus we zijn klaar
        print("Part 2:",loc)
        loc_gev=loc
    loc=loc+1
        
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
