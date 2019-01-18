import io
import hashlib
import logging
import os
import struct
import random

from HintList import getHint, getHintGroup, Hint
from Utils import local_path
from ItemList import eventlocations
from Messages import update_message_by_id

gooditems = [
    'Bow',
    'Progressive Hookshot',
    'Hammer',
    'Slingshot',
    'Boomerang',
    'Bomb Bag',
    'Lens of Truth',
    'Dins Fire',
    'Farores Wind',
    'Nayrus Love',
    'Fire Arrows',
    #'Ice Arrows',
    'Light Arrows',
    'Bottle',
    'Bottle with Letter',
    'Bottle with Milk',
    'Bottle with Red Potion',
    'Bottle with Green Potion',
    'Bottle with Blue Potion',
    'Bottle with Fairy',
    'Bottle with Fish',
    'Bottle with Blue Fire',
    'Bottle with Bugs',
    'Bottle with Poe',
    'Pocket Egg',
    'Pocket Cucco',
    'Cojiro',
    'Odd Mushroom',
    'Odd Potion',
    'Poachers Saw',
    'Broken Sword',
    'Prescription',
    'Eyeball Frog',
    'Eyedrops',
    'Claim Check',
    'Kokiri Sword',
    'Biggoron Sword',
    #'Deku Shield',
    #'Hylian Shield',
    'Mirror Shield',
    'Goron Tunic',
    'Zora Tunic',
    'Iron Boots',
    'Hover Boots',
    'Progressive Strength Upgrade',
    'Progressive Scale',
    'Progressive Wallet',
    'Deku Stick Capacity',
    #'Deku Nut Capacity',
    'Magic Meter',
    #'Double Defense',
    #'Stone of Agony',
    'Zeldas Lullaby',
    'Eponas Song',
    'Suns Song',
    'Sarias Song',
    'Song of Time',
    'Song of Storms',
    'Minuet of Forest',
    'Prelude of Light',
    'Bolero of Fire',
    'Serenade of Water',
    'Nocturne of Shadow',
    'Requiem of Spirit',
]

spoilerHintsList = []


# build a formatted string with linebreaks appropriate textboxes
def buildHintString(hintString):
    if len(hintString) < 77:
        hintString = "They say that " + hintString
    elif len(hintString) < 82:
        hintString = "They say " + hintString
    elif len(hintString) > 91:
        print('Too many characters in hint')
        hintString = hintString[:91]
    hintString = hintString.capitalize()

    formatString = ""
    splitHintString = hintString.split()
    lineLength = 0

    for word in splitHintString:
        # let's assume words are not 35 or more char long
        if lineLength + len(word) + 1 <= 35:
            # add a space if line is not empty
            if lineLength != 0:
                lineLength = lineLength + 1
                formatString = formatString + ' '

            # append word
            formatString = formatString + word
            lineLength = lineLength + len(word)
        else:
            # word won'd fit, add to a new line
            formatString = formatString + '&' + word
            lineLength = len(word)

    return formatString


def getItemGenericName(item):
    if item.type == 'Map' or item.type == 'Compass' or item.type == 'BossKey' or item.type == 'SmallKey':
        return item.type
    else:
        return item.name


def isDungeonItem(item):
    return item.type == 'Map' or item.type == 'Compass' or item.type == 'BossKey' or item.type == 'SmallKey'


def update_hint(messages, id, text):
    update_message_by_id(messages, id, get_raw_text(text))


#builds out general hints based on location and whether an item is required or not
def buildGossipHints(world, messages):

    stoneIDs = [0x0401, 0x0402, 0x0403, 0x0404, 0x0405, 0x0406, 0x0407, 0x0408,
                0x0409, 0x040A, 0x040B, 0x040C, 0x040D, 0x040E, 0x040F, 0x0410,
                0x0411, 0x0412, 0x0413, 0x0414, 0x0415, 0x0416, 0x0417, 0x0418,
                0x0419, 0x041A, 0x041B, 0x041C, 0x041D, 0x041E, 0x041F, 0x0420]

    #shuffles the stone addresses for randomization, always locations will be placed first and twice
    random.shuffle(stoneIDs)

    spoilerHintsList.append('-Way of the Hero-')
    # add required items locations for hints (good hints)
    requiredSample = []
    requiredSample1 = world.spoiler.required_locations
    #print([(location.parent_region.name, location.item.name) for location in requiredSample])
    # loop through the locations we got for "always required locatiosns"
    # if you find lens, remove it
    for l in requiredSample1:
        if l.item.name in ['Lens of Truth', 'Master Sword', 'Stone of Agony']:
            continue
        else:
            requiredSample.append(l)
    #print([(location.parent_region.name, location.item.name) for location in requiredSample])
    if len(requiredSample) >= 4:
        requiredSample = random.sample(requiredSample, 4) #Pick exactly 4
    for location in requiredSample:
        for _ in range(0,3): #and distribute each 3 times (12 / 32)
            if location.parent_region.dungeon:
                update_hint(messages, stoneIDs.pop(0), buildHintString(getHint(location.parent_region.dungeon.name).text + \
                    " is on the way of the hero."))
                spoilerHintsList.append(location.parent_region.dungeon.name + ': ' + location.item.name)
                #print(location.parent_region.dungeon.name, ': ', location.item.name)
            else:
                update_hint(messages, stoneIDs.pop(0), buildHintString(location.parent_region.name + " is on the way of the hero."))
                spoilerHintsList.append(location.parent_region.name + ": " + location.item.name)
                #print(location.parent_region.name, ': ', location.item.name)
    # Don't repeat hints
    checkedLocations = []

    spoilerHintsList.append('\n-Required Locations-')
    # Add required location hints
    alwaysLocations = getHintGroup('alwaysLocation', world)
    for hint in alwaysLocations:
        for locationWorld in world.get_locations():
            if hint.name == locationWorld.name:
                checkedLocations.append(hint.name)
                for _ in range(0,2): #populate each of these twice (24 / 32)
                    update_hint(messages, stoneIDs.pop(0), getHint(locationWorld.name).text + " " + \
                        getHint(getItemGenericName(locationWorld.item)).text + ".")
                    spoilerHintsList.append(locationWorld.name + ": " + locationWorld.item.name)

##    spoilerHintsList.append('\n-Good Locations-')
##    # Add good location hints
##    sometimesLocations = getHintGroup('location', world)
##    if sometimesLocations:
##        # for _ in range(0, random.randint(9,10) - len(alwaysLocations)):
##        for _ in range(0, 2): # Exactly 2 of these (26 / 
##            hint = random.choice(sometimesLocations)
##            # Repick if location isn't new
##            while hint.name in checkedLocations or hint.name in alwaysLocations:
##                hint = random.choice(sometimesLocations)
##
##            for locationWorld in world.get_locations():
##                if hint.name == locationWorld.name:
##                    checkedLocations.append(locationWorld.name)    
##                    update_hint(messages, stoneIDs.pop(0), getHint(locationWorld.name).text + " " + \
##                        getHint(getItemGenericName(locationWorld.item)).text + ".")
##                    spoilerHintsList.append(locationWorld.name + ': ' + locationWorld.item.name)

##    spoilerHintsList.append('\n-BadItem Dungeon-')
##    # add bad dungeon locations hints
##    for dungeon in random.sample(world.dungeons, 2): # Exactly 2 of these (28 / 32)
##        # Choose a randome dungeon location that is a non-dungeon item
##        locationWorld = random.choice([location for region in dungeon.regions for location in world.get_region(region).locations
##            if location.item.type != 'Event' and \
##            not location.name in eventlocations and \
##            not isDungeonItem(location.item) and \
##            (world.tokensanity != 'off' or location.item.name != 'Gold Skulltulla Token') and\
##            location.item.type != 'Song'])
##
##        checkedLocations.append(locationWorld.name)
##        update_hint(messages, stoneIDs.pop(0), buildHintString(getHint(dungeon.name).text + \
##            " hoards " + getHint(getItemGenericName(locationWorld.item)).text + "."))
##        spoilerHintsList.append(dungeon.name + ': ' + locationWorld.item.name) 
##
##    spoilerHintsList.append('\n-BadItem Overworld-')
##    # add bad overworld locations hints
##    # only choose location if it is new and a proper item from the overworld
##    overworldlocations = [locationWorld for locationWorld in world.get_locations()
##            if not locationWorld.name in checkedLocations and \
##            not locationWorld.name in alwaysLocations and \
##            not locationWorld.name in sometimesLocations and \
##            locationWorld.item.type != 'Event' and \
##            not locationWorld.name in eventlocations and \
##            (world.tokensanity == 'all' or locationWorld.item.name != 'Gold Skulltulla Token') and \
##            not locationWorld.parent_region.dungeon and \
##            not locationWorld.name in checkedLocations]
##    overworldSample = overworldlocations
##    if len(overworldSample) >= 2: # Only need to check for 2
##        overworldSample = random.sample(overworldlocations, 2) # Exactly 2 of these (30 / 32)
##    for locationWorld in overworldSample:
##        checkedLocations.append(locationWorld.name)
##        update_hint(messages, stoneIDs.pop(0), buildHintString(getHint(getItemGenericName(locationWorld.item)).text + \
##            " can be found at " + locationWorld.parent_region.name + "."))
##        spoilerHintsList.append(locationWorld.parent_region.name + ': ' + locationWorld.item.name)

    #Populate 4 bad item hints
    spoilerHintsList.append('\n-Bad Items-')
    # add good item hints
    # only choose location if it is new and a good item
    if world.shuffle_weird_egg:
        gooditems.append('Weird Egg')
    baditemlocations = [locationWorld for locationWorld in world.get_locations() 
            if not locationWorld.name in checkedLocations and \
            not locationWorld.name in alwaysLocations and \
            (world.tokensanity == 'all' or locationWorld.item.name != 'Gold Skulltulla Token') and \
            locationWorld.item.type != 'Event' and \
            not locationWorld.name in eventlocations and \
            not isDungeonItem(locationWorld.item) and \
            locationWorld.item.name not in gooditems]
    baditemSample = random.sample(baditemlocations, 4)
    # Don't need this check, we'll fill the rest from this pool, usually only 2, can be more in very rare cases
    # if len(gooditemSample) >= 5:
    #    gooditemSample = random.sample(gooditemlocations, random.randint(3,5))
    # for locationWorld in gooditemSample:
    for locationWorld in baditemSample:
        #locationWorld = gooditemSample.pop()
        checkedLocations.append(locationWorld.name)
        if locationWorld.parent_region.dungeon:
            update_hint(messages, stoneIDs.pop(0), buildHintString(getHint(locationWorld.parent_region.dungeon.name).text + \
                " hoards " + getHint(getItemGenericName(locationWorld.item)).text + "."))
            spoilerHintsList.append(locationWorld.parent_region.dungeon.name + ': ' + locationWorld.item.name)
        else:
            update_hint(messages, stoneIDs.pop(0), buildHintString(getHint(getItemGenericName(locationWorld.item)).text + \
                " can be found at " + locationWorld.parent_region.name + "."))
            spoilerHintsList.append(locationWorld.parent_region.name + ': ' + locationWorld.item.name)
            
    spoilerHintsList.append('\n-Good Items-')
    # add good item hints
    # only choose location if it is new and a good item
    if world.shuffle_weird_egg:
        gooditems.append('Weird Egg')
    gooditemlocations = [locationWorld for locationWorld in world.get_locations() 
            if not locationWorld.name in checkedLocations and \
            locationWorld.item.name in gooditems]
    gooditemSample = gooditemlocations
    # Don't need this check, we'll fill the rest from this pool, usually only 2, can be more in very rare cases
    # if len(gooditemSample) >= 5:
    #    gooditemSample = random.sample(gooditemlocations, random.randint(3,5))
    # for locationWorld in gooditemSample:
    random.shuffle(gooditemSample)
    while stoneIDs:
        locationWorld = gooditemSample.pop()
        checkedLocations.append(locationWorld.name)
        if locationWorld.parent_region.dungeon:
            update_hint(messages, stoneIDs.pop(0), buildHintString(getHint(locationWorld.parent_region.dungeon.name).text + \
                " hoards " + getHint(getItemGenericName(locationWorld.item)).text + "."))
            spoilerHintsList.append(locationWorld.parent_region.dungeon.name + ': ' + locationWorld.item.name)
        else:
            update_hint(messages, stoneIDs.pop(0), buildHintString(getHint(getItemGenericName(locationWorld.item)).text + \
                " can be found at " + locationWorld.parent_region.name + "."))
            spoilerHintsList.append(locationWorld.parent_region.name + ': ' + locationWorld.item.name)

    #spoilerHintsList.append('\n-Junk-\n')
    
    f = open("hints.txt","w")
    f.write('~~~ NEW HINTS ~~~\n\n')
    f.write('\n'.join(spoilerHintsList))
    f.close()
    
    #print(*spoilerHintsList, sep='\n')
    # We don't need this anymore
    # fill the remaining hints with junk    
##    junkHints = getHintGroup('junkHint', world)
##    random.shuffle(junkHints)
##    while stoneIDs:
##        update_hint( messages, stoneIDs.pop(0), junkHints.pop().text )

# builds boss reward text that is displayed at the temple of time altar for child and adult, pull based off of item in a fixed order.
def buildBossRewardHints(world, messages):
    bossRewardsSpiritualStones = ['Kokiri Emerald', 'Goron Ruby', 'Zora Sapphire']
    bossRewardsMedallions = ['Forest Medallion', 'Fire Medallion', 'Water Medallion', 'Shadow Medallion', 'Spirit Medallion', 'Light Medallion']

    # text that appears at altar as a child.
    text = '\x08'
    text += get_raw_text(getHint('Spiritual Stone Text Start').text)
    for reward in bossRewardsSpiritualStones:
        text += buildBossString(reward, world)

    text = setRewardColor(text)
    text += get_raw_text(getHint('Spiritual Stone Text End').text)
    text += '\x0B'

    update_message_by_id(messages, 0x707a, text, 0x20)


    # text that appears at altar as an adult.
    start = '\x08When evil rules all, an awakening\x01voice from the Sacred Realm will\x01call those destined to be Sages,\x01who dwell in the \x05\x41five temples\x05\x40.\x04'
    text = ''
    for reward in bossRewardsMedallions:
        text += buildBossString(reward, world)

    text = setRewardColor(text)
    text += get_raw_text(getHint('Medallion Text End').text)
    text += '\x0B'

    update_message_by_id(messages, 0x7057, start + text, 0x20)

# pulls text string from hintlist for reward after sending the location to hintlist.
def buildBossString(reward, world):
    text = ''
    for location in world.get_locations():
        if location.item.name == reward:
            text += '\x08' + get_raw_text(getHint(location.name).text)
    return text

# alternates through color set commands in child and adult boss reward hint strings setting the colors at the start of the string to correspond with the reward found at the location.
# skips over color commands at the end of stings to set color back to white.
def setRewardColor(text):
    rewardColors = ['\x42', '\x41', '\x43', '\x45', '\x46', '\x44']

    colorWhite = True
    for i, char in enumerate(text):
        if char == '\x05' and colorWhite:
            text = text[:i + 1] + rewardColors.pop(0) + text[i + 2:]
            colorWhite = False 
        elif char == '\x05' and not colorWhite:
            colorWhite = True
        
    return text

# fun new lines for Ganon during the final battle
def buildGanonText(world, messages):
    # empty now unused messages to make space for ganon lines
    update_message_by_id(messages, 0x70C8, " ")
    update_message_by_id(messages, 0x70C9, " ")
    update_message_by_id(messages, 0x70CA, " ")

    # lines before battle
    text = '\x08'
    ganonLines = getHintGroup('ganonLine', world)
    random.shuffle(ganonLines)
    text = get_raw_text(ganonLines.pop().text)
    update_message_by_id(messages, 0x70CB, text)

    # light arrow hint or validation chest item
    text = '\x08'
    if world.trials == 0:
        for location in world.get_locations():
            if location.item.name == 'Light Arrows':
                text = get_raw_text(getHint('Light Arrow Location').text)
                text += get_raw_text(location.hint)
                text += '!'
                break
    else:
        text = get_raw_text(getHint('Validation Line').text)
        for location in world.get_locations():
            if location.name == 'Ganons Tower Boss Key Chest':
                text += get_raw_text(getHint(location.item.name).text)
    
    update_message_by_id(messages, 0x70CC, text)
        
def get_raw_text(string):
    text = ''
    for char in string:
        if char == '^':
            text += '\x04' # box break
        elif char == '&':
            text += '\x01' #new line
        elif char == '@':
            text += '\x0F' #print player name
        elif char == '#':
            text += '\x05\x40' #sets color to white
        else:
            text += char
    return text
