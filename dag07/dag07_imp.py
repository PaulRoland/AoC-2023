# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 05:55:45 2023

@author: Paul
"""

import time
start_time = time.time_ns()

def get_rank_lists(hands):
    result_list1=list()
    result_list2=list()
    
    # 0:high card,1: one pair,2: two pair,3: three of a kind,4: full house,5: four of a kind,6: five of a kind
    # Wat kun je bereiken op basis van het huidige resultaat en een n aantal normale kaarten => normal_card_map[strength][#kaarten] 
    normal_card_map=[[0,0,1,3,5,6],[1,1,2,4],[2,2],[3,3,4],[4],[5,5],[6]]
    
    # Wat kun je bereiken met een bepaalde sterkte en een aantal jokers [strength][#jokers] => joker_effect[strength][#kaarten] 
    joker_effect=[[0,1,3,5,6,6],[1,3,5,6],[2,4],[3,5,6],[4],[5,6],[6]] 
    
    mapping_table_nojoker = str.maketrans({'A': 'Z', 'K': 'Y', 'T': 'F'})  #23456789TJQKA wordt 23456789FJQYZ, mooi op 'alfabetische' volgorde dus
    mapping_table_joker =str.maketrans({'J': '1'}) #23456789TJQKA wordt icm bovenstaande 23456789F1QYZ mooi op 'alfabetische' volgorde met de joker regel
    
    
    #determine hand strength without jokers
    for hand in hands:
        cards = hand[0].replace('J','')
        strength =0
        for card in set(cards):
            matches = cards.count(card)
            strength=normal_card_map[strength][matches]
            if strength == 2 or strength > 3:
                break #score kan niet meer veranderen, stop met deze loop
    
        #jokertjes verwerken
        matches=hand[0].count('J')
        rank1=str(normal_card_map[strength][matches]) #Verwerken als normale kaart
        rank2=str(joker_effect[strength][matches])    #Verwerken met joker effect
        
        #handen op alfabetische volgorde met een mapping
        hand1=hand[0].translate(mapping_table_nojoker)
        hand2=hand1.translate(mapping_table_joker)
        
        #combineer de rank met de getransleerde hand, maak lijsten samen met bijbehorende bid
        result_list1.append([rank1+hand1,hand[1]])
        result_list2.append([rank2+hand2,hand[1]])
        
    #lijsten sorteren returnen
    return sorted(result_list1),sorted(result_list2)


    
f = open("input_dag7.txt", "r")
hands=list()
for i,line in enumerate(f):
    hand = line.split()
    hands.append([hand[0],int(hand[1])])  #maak lijst [kaarten,bid]
f.close()

list_part1,list_part2 = get_rank_lists(hands) #krijg gesorteerde lijst [kaarten,bid]

result_part1=0
result_part2=0
for i in range(len(list_part1)):
    result_part1=result_part1+(i+1)*list_part1[i][1]
    result_part2=result_part2+(i+1)*list_part2[i][1]
 
 
print("Part 1:",result_part1)
print("Part 2:",result_part2)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
    

