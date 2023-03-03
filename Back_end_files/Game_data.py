# 3/1/2023

cards = {
    "daggers" : ("Daggers", "unit", 2, [["dagger"], ["dagger"], ["dagger"]], 0),
    "bows" : ("Bows", "unit", 2, [["bow"], ["bow"]], 0),
    "shield" : ("Shield", "unit", 3, [["shield"]], 0),
    "wall" : ("Wall", "buildings", 5, [["wall"]], 0),
    "sword": ("Sword", "unit", 6, [["sword"]], 0),
    "ballista": ("Ballista", "buildings", 4, [["ballista"]], 0),
    "wheels": ("Wheels", "unit", 3, [["wheel", "wheel"], ["wheel", "wheel"]], 10),
    "catapult": ("Catapult", "unit", 4, [["catapult"]], 0),
    "bomb": ("Bomb", "unit", 1, [["bomb"]], 0),
}


area_attacks = {
    "catapult ball": (8, 100, "all"),
    "bomb blast": (6, 50, "all")
}


activators= {
    "crown rage" : ("Crown rage", "When the game goes into rush mode. The crown will start moving and attack the opposing crown",
                    "game state", "rush", (["walk_speed", "set" , .2], ["search_unit_type", "set", ("noble")], ["attack_range", "set", 40]), True),
    "dissolve" : ("Dissolve", "This building will dissolve overtime", "timer", 1, [["health", "change", -1]], False),
    "self harm": ("Self harm", "Attacking causes recoil", "check actions", "attacked", [["health", "change", -1]], False)
}


units= {
    "crown": ("Crown", "noble", [], 200, "yellow", 
              [200, 200], 0, 2, 25,
              "all", 200, 200, ["crown rage"]),

    "dagger": ("Dagger", "unit", [], 20, "Grey",
               [4, 4], .6, 1, 2,
               "all", 200, 20, []),

    "shield": ("Shield", "noble", [], 40, "Cyan",
               [30, 30], .5, 3, 0,
               "all", 200, 50, []),

    "bow": ("Bow", "unit", [], 20, "Brown",
            [4, 4], .5, 2, 2,
            "all", 200, 150, []),
    
    "wall": ("Wall", "buildings", [], 60, "Tan",
             [60, 60], 0, 1, 0,
             "all", 200, 20, ["dissolve"]),
    
    "sword": ("Sword", "noble", [], 40, "Red",
              [20, 20], 1, 1.5, 5,
              "all", 200, 30, []),
    
    "ballista": ("Ballista", "buildings", [], 40, "Purple",
                 [15, 15], 0, 2.5, 10,
                 "all", 300, 200, ["dissolve"]),
    
    "wheel": ("Wheel", "unit", [], 30, "#36060a",
              [8, 8], 1, 1.5, 1,
              ("buildings", "noble"), 200, 20, []),
    
    "catapult" : ("Catapult", "unit", [], 40, "orange",
                  [20, 20], .3, 3, "catapult ball",
                  "all", 200, 150, []),
    
    "bomb": ("Bomb", "unit", ["attack_area_on_death", "no attack"], 10, "black",
             [1, 1], 1, .2, "bomb blast",
             "all", 200, 30, ["self harm"]) 
    
}