# 3/1/2023

cards = {
    "card units": {
        "daggers": ("Daggers", "unit", 2, [["dagger"], ["dagger"], ["dagger"]], 0),
        "bows": ("Bows", "unit", 2, [["bow"], ["bow"]], 0),
        "shield": ("Shield", "unit", 3, [["shield"]], 0),
        "wall": ("Wall", "buildings", 5, [["wall"]], 0),
        "sword": ("Sword", "unit", 6, [["sword"]], 0),
        "ballista": ("Ballista", "buildings", 4, [["ballista"]], 0),
        "wheels": ("Wheels", "unit", 3, [["wheel", "wheel"], ["wheel", "wheel"]], 10),
        "catapult": ("Catapult", "unit", 4, [["catapult"]], 0),
        "bomb": ("Bomb", "unit", 2, [["bomb"]], 0),
        "kitchen": ("Kitchen", "building", 4, [["kitchen"]], 0),
        "polish": ("Polish", "unit", 3, [["polish"]], 10),
        "fire blast": ("Fire blast", "spell", 5, [["fire blast dummy"]], 0),
        "shocker" : ("Shocker", "unit", 8, [["shocker"]], 0),
        "axe" : ("Axe", "unit", 6, [["axe"]], 0)
        },

    "card crowns": {
        "crown": ("Crown", "crown", 3, [["crown"]], 0),
        "twins": ("Twins", "crown", 3, [["crown twin"], ["crown twin"]], 30),
        "blood crown": ("Blood crown", "crown", 5, [["blood crown"]], 0)
    }
}


activators = {
    "crown rage": ("Crown rage",
                   "When the game goes into rush mode. The crown will start moving and attack the opposing crown",
                   "game state", "rush", (["walk_speed", "set", .2], ["search_unit_type", "set", ["noble", "crown"]]), True),
    "dissolve": ("Dissolve", "This building will dissolve overtime", "timer", 1, [["health", "change", -1]], False),
    "self harm": ("Self harm", "Attacking causes recoil", "check actions", "attacked", [["health", "change", -1]],
                  False),
    "summon knife": ("Summon knife", "Summon a knife every 2 seconds", "timer", 2, [[None, "spawn", ("knife", [0, 0])]],
                     False),

    "blood lust" : ("Blood lust", "Upon killing a unit, this unit will gain +1 to all attacks permanently", "check actions", "killed", [[None, "add status", "blood thirst"]], False)
}

attacks = {
    "crown gun" : ("Crown gun", "Every crown needs a something to stave off those pesky Daggers.",
                   ["crown gun"], ["all"], True, [], [],  
                   25, 400, None, "self", 1, 2),
    
    "crown blade" : ("Crown sword", "Now things get serious", 
                     ["crown blade"], ["crown", "noble"], True, [], [],  
                     25, 240, None, "self", 1, 2),

    "twin crown gun" : ("Twin crown gun", "Every crown needs a something to stave off those pesky Daggers.",
                   ["crown gun"], ["all"], True, [], [],  
                   9, 300, None, "self", 1, 2),
    
    "twin crown blade" : ("Twin crown sword", "Now things get serious", 
                     ["crown blade"], ["crown", "noble"], True, [], [],  
                     9, 240, None, "self", 1, 2),
    
    "dagger stab" : ("Dagger stab", "Poke.", 
                     [], "_parent", True, [], [],
                     2, 40, None, "self", 1, 1),
    
    "bow arrow" : ("Bow Arrow", "Tink.", 
                   [], "_parent", True, [], [],
                   2, 190, None, "self", 1, 2),
    
    "sword slash" : ("Sword slash", "A pristine cut for a pristine steak",
                     [], "_parent", True, [], [],
                     6, 70, None, "self", 1, 1.5),
    
    "ballista bolt" : ("Ballista Bolt", "I was in front of a bolt once.",
                       [], "_parent", True, [], [],
                       10, 240, None, "self", 1, 2.5),
    
    "catapult ball" : ("Catapult ball", "How did they manage to get stone to explode?",
                       [], "_parent", True, [], [],
                       8, 190, 100, "target", 1, 3),

    "wheel bump" : ("Wheel bump", "A frontal assault on any nobility in it's way",
                    [], "_parent", True, [], [],
                    1, 50, None, "self", 1, 1.5),

    "bomb tick" : ("Bomb tick", "It's rage is harmful",
                   [], "_parent", True, [], [],
                   0, 40, None, "self", 1, 1),

    "bomb blast" : ("Bomb blast", "Kaboom!",
                    ["bomb explode"], "_parent", True, [], [],
                    10, 40, 60, "self", 1, 1),
    
    "knife stab" : ("Knife stab", "Poke",
                    [], "_parent", True, [], [],
                    1, 20, None, "self", 1, 1),

    "polish splash" : ("Polish Splash", "Splash and now healed",
                       [], "_parent", True, "_parent", [],
                       -1, 40, None, "self", 1, 1),
    
    "fire blast" : ("Fire blast", "A big explosion fit for a master.",
                    ["bomb explode"], "_parent", True, [], [],
                    10, 60, 140, "self", 1, 1),

    "shock bolts" : ("Shock bolts", "Stings does it?",
                     [], ["all"], False, [], [],
                     1, 120, 120, "self", 10, .5),

    "axe swing" : ("Axe swing", "Hit all your enemies",
                   [], "_parent", True, [], [],
                   6, 40, 80, "self", 30, 1.2),

    "blood sacrifice" : ("Blood sacrifice", "Take the souls of your allies for power",
                         ["crown gun"], ["unit", "noble"], True, ["search allies", "attack allies",], [],
                         1, 400, None, "self", 1, .5),

    "blood axe" : ("Blood axe", "Your rage consumes you.",
                   ["crown blade"], ["all"], True, [], [],
                   1, 220, None, "self", 1, 4)
}

status_effects = {
    "blood thirst" : ("Blood thirst", "?", [], "permanent add", "damage", 1)
}

conditions = {
    "crown gun" : ("not game state", "rush"),
    "crown blade" : ("game state", "rush"),
    "bomb explode" : ("dead", None)
}


units = {
    "crown": ("Crown", "crown", [], 200, "yellow", 
              [200, 200], 0, ["crown gun", "crown blade"],
              ["all"], 200, ["crown rage"]),

    "crown twin": ("Crown duo", "crown", [], 100, "yellow",
                   [100, 100], 0, ["twin crown gun", "twin crown blade"], 
                   ["all"], 200, ["crown rage"]),

    "blood crown" : ("Blood crown", "crown", [], 150, "red",
                     [200, 200], 0, ["blood sacrifice", "blood axe"],
                     ["all"], 200, ["crown rage", "blood lust"]),

    "dagger": ("Dagger", "unit", [], 20, "Grey",
               [4, 4], .6, ["dagger stab"],
               ["all"], 200, []),

    "shield": ("Shield", "noble", [], 40, "Cyan",
               [30, 30], .5, [],
               ["all"], 200, []),

    "bow": ("Bow", "unit", [], 20, "Brown",
            [4, 4], .5, ["bow arrow"],
            ["all"], 200, []),
    
    "wall": ("Wall", "buildings", [], 60, "Tan",
             [60, 60], 0, [],
             ["all"], 200, ["dissolve"]),
    
    "sword": ("Sword", "noble", [], 40, "Red",
              [20, 20], 1, ["sword slash"],
              ["all"], 200, []),
    
    "ballista": ("Ballista", "buildings", [], 40, "Purple",
                 [15, 15], 0, ["ballista bolt"],
                 ["all"], 300, ["dissolve"]),
    
    "wheel": ("Wheel", "unit", [], 30, "#36060a",
              [8, 8], 1, ["wheel bump"],
              ["buildings", "noble"], 200, []),
    
    "catapult": ("Catapult", "unit", [], 40, "orange",
                 [20, 20], .3, ["catapult ball"],
                 ["all"], 200, []),
    
    "bomb": ("Bomb", "unit", ["attack_area_on_death", "no attack"], 10, "black",
             [3, 3], 1, ["bomb tick", "bomb blast"],
             ["all"], 200, ["self harm"]),

    "kitchen": ("Kitchen", "building", [], 40, "silver",
                [20, 20], 0, [],
                ["all"], 10, ["dissolve", "summon knife"]),

    "knife": ("Knife", "unit", [], 10, "silver",
              [2, 2], .8, ["knife stab"],
              ["all"], 200, []),
    
    "polish": ("Polish", "unit", ["search allies", "attack allies", "search injured"], 20, "black",
               [3, 3], .6, ["polish splash"],
               ["unit"], 200, []),

    "fire blast dummy": ("Fire blast dummy", "spell", ["attack_area_on_death", "no attack"], 60, "grey",
                         [2, 2], 0, ["fire blast"],
                         ["all"], 1, ["dissolve"]),

    "shocker" : ("Shocker", "unit", [], 80, "cyan",
                 [60, 60], .4, ["shock bolts"],
                 [], 180, []),

    "axe" : ("Axe", "unit", [], 40, "silver",
             [15, 15], 1.1, ["axe swing"],
             ["all"], 200, [])
}

"""
Flags so far:
attack_area_on_death : The unit will attack with their area attack when killed

attacking -
no attack : The unit can't attack
attack allies : The unit will only attack units in it's team

searching - 
search allies : The unit will only target allies

filters -
search injured : a filter to only attack injured units

"""
