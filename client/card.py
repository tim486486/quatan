'''
Created on Apr 4, 2020

@author: timti
'''
class Card:
    def __init__(self, 
                 deck, 
                 location, 
                 card, 
                 position,
                 rotation):
        self.deck = deck
        self.location = location
        self.card = card
        self.position = position
        self.rotation = rotation