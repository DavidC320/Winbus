# 2/23/2023
import pygame

class Card:
    def __init__(self, name, card_type, coin_cost, unit):
        self.name= name
        self.card_type= card_type
        self.coin_cost= coin_cost
        
        self.unit= unit
        
def create_card(name):
    card = cards.get(name)
    if card:
        return Card(card[0], card[1], card[2], card[3])

cards = {
    "dagger" : ("Dagger", "offense", 1, "dagger"),
    "bow" : ("Bow", "offense", 2, "bow"),
    "shield" : ("Shield", "defense", 3, "shield")
}
