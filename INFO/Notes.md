# Notes

## Spells

Spells will allow the players quick counters to their opponents pushes.

To make this I need to do a couple of things first.

1. Take away the player field restraint from the cursors so that the player can place spells.
2. Have separate how units and spells will work
   1. Spells will ignore units inside of the cursor
   2. units can only place when their are no units inside of the cursor

Spells will basically be still units that blast anything within it's range with damage or an effect. so they will work like bombs with a set timer using health
Spells can't be targeted by anything.

1. Create 1 damage spell
   1. This will use a blast attack object to get this done
2. Create 1 healing spell
   1. This will use a blast attack object to also get this done

## Healing units from other units

To get this to work I need make a way for units to only target their team members and the crown but they can't hit the crown so they just stand their waiting for a team member to heal

I will need a flag so that says the unit can only attack allies and search for allies which should be easy just need to add the unit's ally team to search through

---

## Making building... Again

So all my work got restarted after leaving school so that sucks, but I can remember what I need to do to get this back up again.

### New effect condition

The new effect to get this to work is the spawn effect since activators already exists.

    (None, # skill is None because it's not used
    "spawn", # operation 
    ("unit name", # what unit to grab from the units list
    [0, 0] # positional offset
    ))

### Send created units to the field

in order to get these units to the field I need to get them to the player add unit functions in the player team so to do that quickly I will add a new variable just to store the new units then get them from the unit in unit move

---

## Getting unit groups working

Winbus is now playable, The player can place units on the field and watch them fight the other players units. But I need to figure out a way to place multiple units using one card.

So here is what I was thinking of using a matrix system to do this.

    units= [
        [dagger, dagger, dagger],
        [dagger, dagger, dagger],
        [dagger, dagger, dagger]
    ]

    units= [
        [dagger, dagger],
        [dagger, dagger]
    ]

To get this to work I need to temporarily initialize the units to get their size so that it can be used in positioning.
Here is how it works the game will get the row length and column length

---

### Solution #1

The problem with creating units is that the position is set as center which makes topleft useless so the x and y would need to be halved.

    Sample example

    unit group= [
        [40, 40,]
        [40, 40]
    ]

    padding= 0
    0 + 40 + 0 + 40 + 0
    0 +
    + 0 40 

    80 40 40 160
    80 40 120
    40 80
    40
    -80 -40 40 80
    -40 00 40  = 40 80 120 = 80 + 40 = 120, 40 + 80 = 120, 0 + 120 = 120 
    -40 40 = 40 80 = 40 + 40 = 80, 0 + 80 = 80
    0

    -20 00 20
    -20 20
    0

I need to make a test file to do this.
This will not work do to

---

### Solution #2

I need to get the offsets via blah blah blah

40 40 40

20 "here" 20 | 20 "here" 20 | 20 "here" 20
-80 + 40 = -40 + 40 = 0 + 40 = 40
-40 0 40

40 40

20 "here" 20 | 20 "here" 20
-20 20

40 40 40 40
20 " 20 | 20 " 20 | 20 " 20 | 20 " 20
-60 -20 20 60
