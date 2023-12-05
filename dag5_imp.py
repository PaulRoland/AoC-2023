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


def map_dsr_to_ssd(map_dsr):
#Voer twee maps in met start_stop_delta. De Stop is exclusief deze waarde!
    new_map=[]
    for item in map_dsr:
        new_map.append([item[1],item[1]+item[2],item[0]-item[1]])
    if min(new_map)[0] !=0:
        new_map.append([0,min(new_map)[0],0])
    if max(new_map)[1] !=99999999999:
        new_map.append([max(new_map)[1],99999999999,0])
    
    #Gewoon de mappings compleet maken dat scheelt heel veel drama namelijk
    #controleer of er voor alles een mapping is
    testmap=sorted(new_map)
    for i in range(len(new_map)-1):
        if testmap[i][1]!=testmap[i+1][0]:
            new_map.append([testmap[i][1],testmap[i+1][0],0])
    return sorted(new_map)


def combine_map_ssd(map1,map2):
    new_map = []
    for mapje1 in map1:
        min_map=mapje1[0]
        for mapje2 in map2:
            if min_map+mapje1[2]>=mapje2[0] and min_map+mapje1[2]<mapje2[1]: #startpunt+mapping valt binnen een bepaalde range. Maar wat als het startpunt niet in de range valt maar het eindpunt wel!
                if mapje1[1]<=mapje2[1]-mapje1[2]: #max waarde na mapping valt binnen de huidige range
                    new_map.append([min_map,mapje1[1],mapje1[2]+mapje2[2]]) #alles valt er dus binnen, dus deze mappings combineren volledig
                    break #klaar met dit item! Yippie
                else:
                    new_map.append([min_map,mapje2[1]-mapje1[2],mapje1[2]+mapje2[2]]) #Combineer mappings op de overlap mogelijk
                    min_map=mapje2[1]-mapje1[2] #We gaan door met een nieuwe minimum waarde omdat een stukje overlappend was, maar er nog een stukje over is
    return new_map


def apply_map_ranges(ranges,map_ssd):
    #ranges (start,stop)
    new_ranges=[]
    for cur_range in ranges:
        min_range=cur_range[0]
        for mapping in map_ssd:
            if min_range >= mapping[0] and min_range < mapping[1]: #Current range valt binnen de waardes van de mapping
                if cur_range[1]<mapping[1]: #Maximum valt binnen het bereik van de mapping functie
                    new_ranges.append([cur_range[0]+mapping[2],cur_range[1]+mapping[2]])
                    break
                else:
                    new_ranges.append([min_range+mapping[2],mapping[1]-1+mapping[2]]) #Apply mapping to the current range and the highest allowed value (mapping1 -1) continue code with this value
                    min_range=mapping[1]
    return new_ranges


def apply_map_values(values,map_ssd):
    mapped_values=[]
    for value in values:
        for mapping in map_ssd:
            if value >= mapping[0] and value < mapping[1]: #Current value valt binnen de waardes van de mapping
                mapped_values.append(value+mapping[2])
                break
  
    return mapped_values

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
soil_map =map_dsr_to_ssd(seed_soil)
fert_map =map_dsr_to_ssd(soil_fert)
water_map=map_dsr_to_ssd(fert_water)
light_map=map_dsr_to_ssd(water_light)
temp_map = map_dsr_to_ssd(light_temp)
hum_map  = map_dsr_to_ssd(temp_hum)
loc_map  = map_dsr_to_ssd(hum_loc)
    
loc_list=list()

#combine soil_map and fert_map and check results
all_maps=combine_map_ssd(combine_map_ssd(combine_map_ssd(combine_map_ssd(combine_map_ssd(combine_map_ssd(soil_map,fert_map),water_map),light_map),temp_map),hum_map),loc_map)

#Find the locations of the seeds
locations = apply_map_values(seed_list,all_maps)
print("Dag 5 Part 1:", min(locations))

#De lijst met zaden moeten ranges zijn! Wauw wat een ontdekking
seed_ranges=[]
for i in range(10):
    seed_ranges.append([seed_list[2*i],int(seed_list[2*i])+int(seed_list[2*i+1])])

locations_ranges = apply_map_ranges(seed_ranges,all_maps)
print("Dag 5 Part 2:", min(locations_ranges)[0])

print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))