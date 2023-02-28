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
    "dagger" : ("Dagger", "unit", 1, "dagger"),
    "bow" : ("Bow", "unit", 2, "bow"),
    "shield" : ("Shield", "unit", 3, "shield"),
    "wall" : ("Wall", "tower", 5, "wall"),
    "sword": ("Sword", "unit", 6, "sword"),
    "ballista": ("Ballista", "unit", 5, "ballista")
}
