# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 05:55:45 2023

@author: Paul
"""

import time
start_time = time.time_ns()


import numpy as np
from operator import itemgetter, attrgetter

class card_class:
    def __init__(self,strength,card,bid,new_card):
        self.strength=strength
        self.card=card
        self.bid=bid
        self.new_card=new_card
    def __repr__(self):
        return repr((self.strength, self.card, self.bid,self.new_card))

def get_rank(cards):
    strength = 0
    for card in set(cards):
        matches = cards.count(card)
        if matches ==5:
            strength = 6
            break  #five of a kind
        if matches==4:
            strength= 5
            break #four of a kind
        if matches==3:
            if strength==1:
                strength = 4  #full house
                break #full house
            strength=3  #three of a kind
        if matches==2:
            if strength==3:
                strength = 4
                break #full house   
            else:
                strength=strength+1 #one pair of two pairs
            
    return strength

def get_rank_joker(cards):
    strength = 0
    card_joker=cards.replace('J','')
    for card in set(card_joker):
        matches = cards.count(card)
        if matches ==5:
            strength = 6
            break  #five of a kind
        if matches==4:
            strength= 5
            break #four of a kind
        if matches==3:
            if strength==1:
                strength = 4  #full house
                break #full house
            strength=3  #three of a kind
        if matches==2:
            if strength==3:
                strength = 4
                break #full house   
            else:
                strength=strength+1 #one pair of two pairs
    
    joker_effect=[[0,1,3,5,6,6],[1,3,5,6],[2,4],[3,5,6],[4],[5,6],[6]] #Takes current strength and uses jokers
    return joker_effect[strength][cards.count('J')]

def change_card(card):
    carddict={'2':'a',
              '3':'b',
              '4':'c',
              '5':'d',
              '6':'e',
              '7':'f',
              '8':'g',
              '9':'h',
              'T':'i',
              'J':'j',
              'Q':'k',
              'K':'l',
              'A':'m'}
    new_card=''
    for characters in card:
        new_card=new_card+carddict[characters]
    return new_card

def change_card_joker(card):
    carddict={'2':'b',
              '3':'c',
              '4':'d',
              '5':'e',
              '6':'f',
              '7':'g',
              '8':'h',
              '9':'i',
              'T':'j',
              'J':'a',
              'Q':'k',
              'K':'l',
              'A':'m'}
    new_card=''
    for characters in card:
        new_card=new_card+carddict[characters]  
    return new_card


    
f = open("input_dag7.txt", "r")
total_rank_sum=0
cards=list()
cards_joker=list()
for i,line in enumerate(f):
    card=line.split(' ')
    cards_joker.append(card_class(get_rank_joker(card[0]),card[0],int(card[1]),change_card_joker(card[0])))
    cards.append(card_class(get_rank(card[0]),card[0],int(card[1]),change_card(card[0])))
f.close()

sorted_cards = sorted(cards,key=attrgetter('strength','new_card'))
for i,cards in enumerate(sorted_cards):
    total_rank_sum=total_rank_sum+(i+1)*cards.bid
print(total_rank_sum)

total_rank_sum=0
sorted_cards = sorted(cards_joker,key=attrgetter('strength','new_card'))
for i,cards in enumerate(sorted_cards):
    total_rank_sum=total_rank_sum+(i+1)*cards.bid
    
print(total_rank_sum)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
