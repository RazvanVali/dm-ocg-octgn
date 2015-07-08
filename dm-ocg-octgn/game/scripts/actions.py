#------------------------------------------------------------------------------
# Constant and Variables Values
#------------------------------------------------------------------------------
import re
import itertools

shields = []
playerside = None
sideflip = None
diesides = 20
shieldMarker = ('Shield', 'a4ba770e-3a38-4494-b729-ef5c89f561b7')

# Start of Automation code

# These effects activate when the corresponding creature is summoned
onSummon = {
			'Alshia, Spirit of Novas': 'search(me.piles[\'Graveyard\'], 1, "Spell")',
			'Akashic Second, Electro-Spirit': 'draw(me.Deck, True);',
			'Aqua Bouncer': 'bounce()',
			'Aqua Deformer': 'fromMana(2)',#; remoteCall(not card.owner==me,"fromMana",2)',
			'Aqua Hulcus': 'draw(me.Deck, True);',
			'Aqua Sniper': 'bounce(2)',
			'Aqua Surfer': 'bounce()',
			'Armored Decimator Valkaizer': 'kill(4000)',
			'Artisan Picora': 'fromMana(1,"ALL","ALL","ALL",False,True)', #IF COST (or NAME, or other) SEARCH IS IMPLEMENTED THIS SUFFERS CHANGES.
			'Astral Warper': 'draw(me.Deck, True, 3)',
			'Belix, the Explorer': 'fromMana(1,"Spell")',
			'Bronze-Arm Tribe': 'mana(me.Deck);',
			'Chaos Worm': 'kill()',
			'Craze Valkyrie, the Drastic': 'tapCreature(2)',
			'Dandy Eggplant': 'fromDeck()',
			'Dark Hydra, Evil Planet Lord': 'fromGrave()',
			'Estol, Vizier of Aqua': 'shields(me.Deck)',
			'Evolution Totem': 'search(me.Deck, 1, "Evolution Creature")',
			'Factory Shell Q': 'search(me.Deck, 1, "ALL", "ALL", "Survivor")',
			'Fighter Dual Fang': 'mana(me.Deck,2)',
			'Fonch, the Oracle': 'tapCreature()',
			'Forbos, Sanctum Guardian Q': 'search(me.Deck, 1, "Spell")',
			'Funky Wizard': 'draw(me.Deck, True);',
			'Gigargon': 'search(me.piles[\'Graveyard\'], 2, "Creature")',
			'Grave Worm Q': 'search(me.piles[\'Graveyard\'], 1, "ALL", "ALL", "Survivor")',
			'Gyulcas, Sage of the East Wind': 'search(me.Deck, 1, "Cross Gear")',
			'Hawkeye Lunatron': 'search(me.Deck, 1, "ALL", "ALL", "ALL", False)', #IF COST (or NAME, or other) SEARCH IS IMPLEMENTED THIS SUFFERS CHANGES.
			'Hurlosaur': 'kill(1000)',
			'King Ripped-Hide': 'draw(me.Deck, True, 2)',
			'Kolon, the Oracle': 'tapCreature()',
			'Lena, Vizier of Brilliance': 'fromMana(1,"Spell")',
			'Magris, Vizier of Magnetism': 'draw(me.Deck, True);',
			'Meteosaur': 'kill(2000)',
			'Miele, Vizier of Lightning': 'tapCreature()',
			'Moors, the Dirty Digger Puppet': 'search(me.piles[\'Graveyard\'])',
			'Niofa, Horned Protector': 'search(me.Deck, 1, "ALL", "Nature")',
			'Ochappi, Pure Hearted Faerie': 'fromGrave()',
			'Phal Eega, Dawn Guardian': 'search(me.piles[\'Graveyard\'], 1, "Spell")',
			'Rayla, Truth Enforcer': 'search(me.Deck, 1, "Spell")',
			'Rom, Vizier of Tendrils': 'tapCreature()',
			'Rothus, the Traveler': 'sacrifice()',
			'Rumbling Terahorn': 'search(me.Deck, 1, "Creature")',
			'Ryokudou, the Principle Defender': 'mana(me.Deck,2);fromMana()',
			'Scissor Scarab': 'search(1,"ALL","ALL","Giant Insect")',
			'Shtra': 'fromMana()',#; remoteCall(not card.owner,"fromMana",1)',
			'Skysword, the Savage Vizier': 'mana(me.Deck);shields(me.Deck)',
			'Solidskin Fish': 'fromMana()',
			'Spiritual Star Dragon': 'fromDeck()',
			'Splash Zebrafish': 'fromMana()',
			'Syforce, Aurora Elemental': 'fromMana(1,"Spell")',
			'Thorny Mandra': 'fromGrave()',
			'Thrash Crawler': 'fromMana()',
			'Torpedo Cluster': 'fromMana()',
			'Unicorn Fish': 'bounce()',
			'Velyrika Dragon': 'search(me.Deck, 1, "ALL", "ALL", "Armored Dragon")',
			'Whispering Totem': 'fromDeck()',
			'Wind Axe, the Warrior Savage': 'mana(me.Deck)',
			'Zardia, Spirit of Bloody Winds': 'shields(me.Deck)',
    }

# These effects are triggered when the corresponding spell is cast
onCast = {  'Abduction Charger': 'bounce(2)',
            'Apocalypse Day': 'banishALL(table, len([card for card in table if isCreature(card)])>5)',
            'Boomerang Comet': 'fromMana(); toMana(card)',
            'Brain Serum': 'draw(me.Deck, False, 2)',
            'Chains of Sacrifice': 'kill(2); sacrifice()',
            'Clone Factory': 'fromMana(2)',
            'Corpse Charger': 'search(me.piles[\'Graveyard\'], 1, "Creature)',
            'Crimson Hammer': 'kill(2000)',
            'Cyber Brain': 'draw(me.Deck, False, 3)',
            'Crystal Memory': 'search(me.Deck, 1, "ALL", "ALL", "ALL", False)', #IF COST (or NAME, or other) SEARCH IS IMPLEMENTED THIS SUFFERS CHANGES.
            'Dark Reversal': 'search(me.piles[\'Graveyard\'], 1, "Creature")',
            'Death Smoke': 'kill()',
            'Dimension Gate': 'search(me.Deck, 1, "Creature")',
            'Dracobarrier': 'tapCreature()',
            'Enchanted Soil': 'fromGrave()',
            'Energy Stream': 'draw(me.Deck, False, 2)',
            'Eureka Charger': 'draw(me.Deck);',
            'Faerie Life': 'mana(me.Deck);',
            'Flame Lance Trap': 'kill(5000)',
            'Flood Valve': 'fromMana()',
            'Hopeless Vortex': 'kill()',
            'Holy Awe': 'tapCreature(1,True)',
            'Invincible Abyss': 'banishALL([card for card in table if card.owner != me], True)',
            'Invincible Aura': 'shields(me.Deck,3,True)',
            'Invincible Technology': 'search(me.Deck,len(me.Deck))',
            'Lightning Charger': 'tapCreature()',
            'Logic Cube': 'search(me.Deck, 1, "Spell")',
            'Logic Sphere': 'fromMana(1, "Spell")',
            'Miraculous Rebirth': 'kill(5000);fromDeck()',
            'Miraculous Snare': 'sendToShields()',
            'Moonlight Flash': 'tapCreature(2)',
            'Morbid Medicine': 'search(me.piles[\'Graveyard\'], 2, "Creature")',
            'Mystic Dreamscape': 'fromMana(3)',
            'Mystic Inscription': 'shields(me.Deck)',
            'Phantom Dragon\'s Flame': 'kill(2000)',
            'Pixie Cocoon': 'fromMana(1, "Creature");toMana(card)',
            'Punish Hold': 'tapCreature(2)',
            'Purgatory Force': 'search(me.piles[\'Graveyard\'], 2, "Creature")',
            'Reap and Sow': 'mana(me.Deck)',
            'Riptide Charger': 'bounce()',
            'Solar Ray': 'tapCreature()',
            'Solar Trap': 'tapCreature()',
            'Spastic Missile': 'kill(3000)',
            'Spiral Gate': 'bounce()',
            'Stronghold of Lightning and Flame': 'kill(3000); tapCreature()',
            'Teleportation': 'bounce(2)',
            'Ten-Ton Crunch': 'kill(3000)',
            'Terror Pit': 'kill()',
            'Triple Brain': 'draw(me.Deck, False, 3)',
            'Tornado Flame': 'kill(4000)',
            'Ultimate Force': 'mana(me.Deck,2)',
            'Volcanic Arrows': 'kill(6000)',
            'Volcano Charger': 'kill(2000)',
            'Zombie Carnival': 'fromGrave()',
            'Solar Ray': 'tapCreature()',
            'Solar Trap': 'tapCreature()',
            'Lightning Charger': 'tapCreature()',
            'Moonlight Flash': 'tapCreature(2)',
            'Dracobarrier': 'tapCreature()',
            'Clone Factory': 'fromMana(2)',
            'Mystic Dreamscape': 'fromMana(3)',
            'Boomerang Comet': 'fromMana();toMana(card)',
            'Pixie Cocoon': 'fromMana();toMana(card)',
            'Logic Sphere': 'fromManaSpell()',
            'Miraculous Rebirth': 'kill(5000);fromDeck()',
            'Stronghold of Lightning and Flame': 'kill(3000);tapCreature()',
            'Seven\'s Tower': 'if metamorph(): mana(me.Deck,3) else: mana(me.Deck)',
            'Martial Law': 'gear(kill);',
            'Natural Snare': 'sendToMana()',
            'Spiral Lance': 'gear(bounce);',
            'Wave Rifle': 'gear(bounce);',
            'Screw Rocket': 'gear(kill);',
            'Drill Bowgun': 'gear(kill);',
            'Valiant Spark': 'if metamorph(): tapCreature(1,True) else: tapCreature()'
    }

# These effects trigger when creatures are destroyed
onDestroy = {'Akashic First, Electro-Dragon': 'toHand(card)',
             'Akashic Second, Electro-Spirit': 'toMana(card)',
             'Aqua Agent': 'toHand(card)',
             'Aqua Knight': 'toHand(card)',
             'Aqua Ranger': 'toHand(card)',
             'Aqua Skydiver': 'toHand(card)',
             'Aqua Soldier': 'toHand(card)',
             'Asylum, the Dragon Paladin': 'toShields(card)',
             'Bat Doctor, Shadow of Undeath': 'search(me.piles[\'Graveyard\'], 1, "Creature")',
             'Bone Piercer': 'fromMana(1, "Creature")',
             'Cetibols': 'draw(me.Deck, True)',
             'Chillias, the Oracle': 'toHand(card)',
             'Coiling Vines': 'toMana(card)',
             'Crasher Burn': 'kill(3000)',
             'Crystal Jouster': 'toHand(card)',
             'Cubela, the Prophet': 'tapCreature()',
             'Dracodance Totem': 'fromMana(1,"","","Dragon");toMana(card)',
             'Hammerhead Cluster': 'bounce()',
             'Jil Warka, Time Guardian': 'tapCreature(2)',
             'Mighty Shouter': 'toMana(card)',
             'Ouks, Vizier of Restoration': 'toShields(card)',
             'Pharzi, the Oracle': 'search(me.piles[\'Graveyard\'], 1, "Spell")',
             'Proxion, the Prophet': 'toHand(card)',
             'Shaman Broccoli': 'toMana(card)',
             'Shout Corn': 'toMana(card)',
             'Solid Horn': 'toMana(card)',
             'Stubborn Jasper': 'toHand(card)',
             'Red-Eye Scorpion': 'toMana(card)'
    }

# Functions used in the Automation dictionaries.

def fromMana(count = 1, TypeFilter = "ALL", CivFilter = "ALL", RaceFilter = "ALL", show = False, toGrave = False):
	mute()
	for i in range(0,count):
		if TypeFilter != "ALL":
			cardsInGroup_Type_Filtered = [card for card in table if isMana(card) and card.owner==me and re.search(TypeFilter,card.Type)]
		else:
			cardsInGroup_Type_Filtered = [card for card in table if isMana(card) and card.owner==me]
		if CivFilter != "ALL":
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered if re.search(CivFilter,card.properties['Civilization'])]
		else:
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered]
		if RaceFilter != "ALL":
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered if re.search(RaceFilter,card.properties['Race'])]
		else:
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered]
		if len(cardsInGroup_CivTypeandRace_Filtered) == 0: return
		choice = askCard(cardsInGroup_CivTypeandRace_Filtered, 'Choose a Card to return to hand from the Mana Zone','Mana Zone')
		if type(choice) is not Card: break
		if toGrave == True: banish(choice)
		else: toHand(choice, show)

def fromDeck():
    mute()
    notify("{} looks at their Deck.".format(me))
    me.Deck.lookAt(-1)

def fromGrave():
    mute()
    notify("{} looks at their Graveyard.".format(me))
    me.piles['Graveyard'].lookAt(-1)

def kill(power = float('inf'), count = 1):
	mute()
	for i in range(0, count):
		cardList = [card for card in table if isCreature(card) and not card.owner==me and re.search("Creature", card.Type)]
		cardList = [card for card in cardList if int(card.Power) <= power]
		if len(cardList)==0:
			return    
		choice = askCard(cardList, 'Choose a Creature to destroy')
		if type(choice) is not Card:
			return
		remoteCall(choice.owner,"banish",choice)

def sacrifice(power = float('inf'), count = 1):
	mute()
	for i in range(0, count):
		cardList = [card for card in table if isCreature(card) and card.owner==me and re.search("Creature", card.Type)]
		cardList = [card for card in cardList if int(card.Power) <= power]
		if len(cardList)==0:
			return    
		choice = askCard(cardList, 'Choose a Creature to destroy')
		if type(choice) is not Card:
			return
		banish(choice)
    
def bounce(count = 1):
        mute()
        for i in range(0,count):
                cardList = [card for card in table if isCreature(card) and re.search("Creature", card.Type)]
                if len(cardList)==0:
                        return
                choice = askCard(cardList,'Choose a Creature to return to Hand')
                if type(choice) is not Card:
                        return
                if choice.owner==me:
                        toHand(choice)
                else:
                        remoteCall(choice.owner,"toHand",choice)
    
def gear(str):        
    mute()
    if str == 'kill':
        cardList = [card for card in table if isGear(card)
                    and not card.owner == me]
        if len(cardList) == 0:
            return
        choice = askCard(cardList,
                         'Choose a Cross Gear to send to Graveyard')
        if type(choice) is not Card:
            return
        remoteCall(choice.owner, 'banish', choice)
    elif str == 'bounce':
        cardList = [card for card in table if isGear(card)]
        if len(cardList) == 0:
            return
        choice = askCard(cardList, 'Choose a Cross Gear to send to Hand'
                         )
        if type(choice) is not Card:
            return
        if choice.owner == me:
            toHand(choice)
        else:
            remoteCall(choice.owner, 'toHand', choice)
    elif str == 'mana':
        cardList = [card for card in table if isGear(card)]
        if len(cardList) == 0:
            return
        choice = askCard(cardList, 'Choose a Cross Gear to send to Mana'
                         )
        if type(choice) is not Card:
            return
        if choice.owner == me:
            toHand(choice)
        else:
            remoteCall(choice.owner, 'toMana', choice)

def sendToShields():
	mute()
	for i in range(0,count):
		cardList = [card for card in table if isCreature(card) and card.owner != me]
		if len(cardList)==0: return
		choice = askCard(cardList,'Choose a Creature to send to shields')
		if type(choice) is not Card: return
		remoteCall(choice.owner,"toShields",choice)

def sendToMana():
	mute()
	for i in range(0,count):
		cardList = [card for card in table if isCreature(card) and card.owner != me]
		if len(cardList)==0: return
		choice = askCard(cardList,'Choose a Creature to send to mana')
		if type(choice) is not Card: return
		remoteCall(choice.owner,"toMana",choice)

def tapCreature(count = 1, targetALL = False, includeOwn = False):
    mute()
    if targetALL:
        if includeOwn == True: 
            cardList = [card for card in table if isCreature(card) and re.search("Creature", card.Type)]
        else:
            cardList = [card for card in table if isCreature(card) and not card.owner==me and re.search("Creature", card.Type)]
        if len(cardList)==0:
            return
        for card in cardList:
            remoteCall(choice.owner,"tap",choice)
    else:
        for i in range(0,count):
            if includeOwn == True: 
                cardList = [card for card in table if isCreature(card) and re.search("Creature", card.Type)]
            else:
                cardList = [card for card in table if isCreature(card) and not card.owner==me and re.search("Creature", card.Type)]
            if len(cardList)==0:
                return
            choice = askCard(cardList, 'Choose a Creature to tap')
            if type(choice) is not Card:
                return
            remoteCall(choice.owner,"tap",choice)

#End of Automation Code

def resetGame():
    mute()
    me.setGlobalVariable("shieldCount", "0")

def moveCards(player, card, fromGroup, toGroup, oldIndex, index, oldX, oldY, x, y, highlights, markers, faceup):
    ## This trigger updates the evolution dictionary in the event one of the cards involved in an evolution leaves the battlezone.
    mute()
    if player != me: ##Ignore for cards you don't control
        return
    if table not in fromGroup: ## we only want cases where a card is being moved from table to another group
        return
    evolveDict = eval(me.getGlobalVariable("evolution"))
    for evo in evolveDict.keys():
        if Card(evo) not in table:
            del evolveDict[evo]
        else:
            evolvedList = evolveDict[evo]
            for evolvedCard in evolvedList:
                if Card(evolvedCard) not in table:
                    evolvedList.remove(evolvedCard)
            if len(evolvedList) == 0:
                del evolveDict[evo]
            else:
                evolveDict[evo] = evolvedList
    if evolveDict != eval(me.getGlobalVariable("evolution")):
        me.setGlobalVariable("evolution", str(evolveDict))

def isCreature(card):
    mute()
    if card in table and card.isFaceUp and not card.orientation == Rot180 and not card.orientation == Rot270:
        return True
    else:
        return False

def isGear(card):
	mute()
	if card in table and card.isFaceUp and card.orientation == Rot0 and re.search("Cross Gear", card.Type): return True
	else: return False

def isMana(card):
    mute()
    if card in table and card.isFaceUp and not card.orientation == Rot90 and not card.orientation == Rot0:
        return True
    else:
        return False

def isShield(card):
    mute()
    if card in table and not card.isFaceUp:
        return True
    else:
        return False

def metamorph():
    mute()
    cardList = [card for card in table if isMana(card) and card.owner== me]
    if len(cardList) < 7:
        return False
    else:
        return True


def align():
    mute()
    global playerside  ##Stores the Y-axis multiplier to determine which side of the table to align to
    global sideflip  ##Stores the X-axis multiplier to determine if cards align on the left or right half
    if sideflip == 0:  ##the 'disabled' state for alignment so the alignment positioning doesn't have to process each time
        return "BREAK"
    if Table.isTwoSided():
        if playerside == None:  ##script skips this if playerside has already been determined
            if me.hasInvertedTable():
                playerside = -1  #inverted (negative) side of the table
            else:
                playerside = 1
        if sideflip == None:  ##script skips this if sideflip has already been determined
            playersort = sorted(getPlayers(), key=lambda player: player._id)  ##makes a sorted players list so its consistent between all players
            playercount = [p for p in playersort if me.hasInvertedTable() == p.hasInvertedTable()]  ##counts the number of players on your side of the table
            if len(playercount) > 2:  ##since alignment only works with a maximum of two players on each side
                whisper("Cannot align: Too many players on your side of the table.")
                sideflip = 0  ##disables alignment for the rest of the play session
                return "BREAK"
            if playercount[0] == me:  ##if you're the 'first' player on this side, you go on the positive (right) side
                sideflip = 1
            else:
                sideflip = -1
    else:  ##the case where two-sided table is disabled
        whisper("Cannot align: Two-sided table is required for card alignment.")
        sideflip = 0  ##disables alignment for the rest of the play session
        return "BREAK"
    cardorder = [[],[],[]]
    evolveDict = eval(me.getGlobalVariable("evolution"))
    for card in table:
        if card.controller == me and not card._id in list(itertools.chain.from_iterable(evolveDict.values())):
            if isShield(card):
                cardorder[1].append(card)
            elif isMana(card):
                cardorder[2].append(card)
            else: ##collect all creatures
                cardorder[0].append(card)
    xpos = 80
    ypos = 5 + 10*(max([len(evolveDict[x]) for x in evolveDict]) if len(evolveDict) > 0 else 1)
    for cardtype in cardorder:
        if cardorder.index(cardtype) == 1:
            xpos = 80
            ypos += 93
        elif cardorder.index(cardtype) == 2:
            xpos = 80
            ypos += 93
        for c in cardtype:
            x = sideflip * xpos
            y = playerside * ypos + (44*playerside - 44)
            if c.position != (x,y):
                c.moveToTable(x,y)
            xpos += 79
    for evolution in evolveDict:
        count = 0
        for evolvedCard in evolveDict[evolution]:
            x, y = Card(evolution).position
            count += 1
            Card(evolvedCard).moveToTable(x, y - 10*count*playerside)
            Card(evolvedCard).sendToBack()


def clear(card, x = 0, y = 0):
    mute()
    card.target(False)

def setup(group, x = 0, y = 0):
    mute()
    ## cancel out of setup if any of these conditions occur
    for c in table: ## scan the table for cards you own or control
        if c.controller == me or c.owner == me:
            return
    for c in me.hand: ## cancel if you've already drawn cards
        return
    for c in me.piles['Graveyard']: ##cancel if you have cards in Discard
        return
    if len(me.Deck) < 10: #We need at least 10 cards to properly setup the game
        return
    #####
    me.setGlobalVariable("shieldCount", "0")
    me.Deck.shuffle()
    rnd(1,10)
    for card in me.Deck.top(5): toShields(card, notifymute = True)
    for card in me.Deck.top(5): card.moveTo(card.owner.hand)
    align()
    notify("{} sets up their battle zone.".format(me))

def rollDie(group, x = 0, y = 0):
    mute()
    global diesides
    n = rnd(1, diesides)
    notify("{} rolls {} on a {}-sided die.".format(me, n, diesides))

def untapAll(group, x = 0, y = 0):
    mute()
    for card in group:
        if not card.owner == me:
            continue
        if card.orientation == Rot90:
            card.orientation = Rot0
        if card.orientation == Rot270:
            card.orientation = Rot180
    notify("{} untaps all their cards.".format(me))
    
def tap(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify('{} taps {}.'.format(me, card))
    else:
        notify('{} untaps {}.'.format(me, card))

def banish(card, x = 0, y = 0):
	mute()
	if isShield(card):
		card.peek()
		rnd(1,10)
		if re.search("{SHIELD TRIGGER}", card.Rules):
			if confirm("Activate Shield Trigger for {}?\n\n{}".format(card.Name, card.Rules)):
				card.isFaceUp = True
				toPlay(card, notifymute = True)
				rnd(1,10)
				notify("{} uses {}'s Shield Trigger.".format(me, card))
				return
		shieldCard = card
		cardsInHandWithStrikeBackAbility = [card for card in me.hand if re.search("Strike Back", card.rules)]
		if len(cardsInHandWithStrikeBackAbility) > 0:
			cardsInHandWithStrikeBackAbilityThatCanBeUsed = [card for card in cardsInHandWithStrikeBackAbility if shieldCard.properties['Civilization'] == card.properties['Civilization']]
			if len(cardsInHandWithStrikeBackAbilityThatCanBeUsed) > 0:
				if confirm("Activate Strike Back by sending {} to the graveyard?\n\n{}".format(shieldCard.Name, shieldCard.Rules)):
					choice = askCard(cardsInHandWithStrikeBackAbilityThatCanBeUsed, 'Choose Strike Back to activate')
					if type(choice) is Card:
						shieldCard.isFaceUp = True
						rnd(1,100)
						toPlay(choice, notifymute = True)
						toDiscard(shieldCard)
						notify("{} banishes {} to use {}'s Strike Back.".format(me, shieldCard.name, choice.name))
						return
		notify("{}'s shield #{} is broken.".format(me, shieldCard.markers[shieldMarker]))
		shieldCard.moveTo(shieldCard.owner.hand)
	else:
		cardToBeSaved = card
		possibleSavers = [card for card in table if cardToBeSaved != card and isCreature(card) and card.owner == me and re.search("Saver",card.rules) and (re.search(cardToBeSaved.properties['Race'],card.rules) or re.search("Saver: All Races",card.rules))]
		if len(possibleSavers) > 0:
			if confirm("Prevent {}'s destruction by using a Saver on your side of the field?\n\n".format(cardToBeSaved.Name)):
				choice = askCard(possibleSavers, 'Choose Saver to banish')
				if type(choice) is Card:
					toDiscard(choice)
					notify("{} banishes {} to prevent {}'s destruction.".format(me, choice.name, cardToBeSaved.name))
					return
		toDiscard(cardToBeSaved)
		if cardToBeSaved.name in onDestroy:
			exec(onDestroy[cardToBeSaved.name])

def banishALL(group, condition = False, x = 0, y = 0):
	mute()
	if condition == False: return
	cardList = [card for card in group if isCreature(card)]
	if len(cardList)==0: return
	for card in cardList:
		cardToBeSaved = card
		possibleSavers = [card for card in table if cardToBeSaved != card and isCreature(card) and card.owner == me and re.search("Saver",card.rules) and (re.search(cardToBeSaved.properties['Race'],card.rules) or re.search("Saver: All Races",card.rules))]
		if len(possibleSavers) > 0:
			if confirm("Prevent {}'s destruction by using a Saver on your side of the field?\n\n".format(cardToBeSaved.Name)):
				choice = askCard(possibleSavers, 'Choose Saver to banish')
				if type(choice) is Card:
					toDiscard(choice)
					cardList.remove(choice)
					cardList = [card for card in cardList]
					notify("{} banishes {} to prevent {}'s destruction.".format(me, choice.name, cardToBeSaved.name))
					continue
		toDiscard(cardToBeSaved)
		if cardToBeSaved.name in onDestroy:
			exec(onDestroy[cardToBeSaved.name])

def shuffle(group, x = 0, y = 0):
    mute()
    if len(group)==0:return
    for card in group:
        if card.isFaceUp:
            card.isFaceUp = False
    group.shuffle()
    notify("{} shuffled their {}".format(me, group.name))

def draw(group, conditional = False, count = 1, x = 0, y = 0):
    mute()
    for i in range(0,count):
        if len(group) == 0:
            return
        if conditional == True:
            choiceList = ['Yes', 'No']
            colorsList = ['#FF0000', '#FF0000']
            choice = askChoice("Draw a card?", choiceList, colorsList)
            if choice == 0:
                return 
        card = group[0]
        card.moveTo(card.owner.hand)
        notify("{} draws a card.".format(me))

def drawX(group, x = 0, y = 0):
    if len(group) == 0: return
    mute()
    count = askInteger("Draw how many cards?", 7)
    if count == None: return
    for card in group.top(count): card.moveTo(card.owner.hand)
    notify("{} draws {} cards.".format(me, count))
    
def mill(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group[0]
    toDiscard(card, notifymute = True)
    notify("{} discards top card of Deck.".format(me))
    
def millX(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    count = askInteger("Discard how many cards?", 1)
    if count == None: return
    for card in group.top(count): toDiscard(card, notifymute = True)
    notify("{} discards top {} cards of Deck.".format(me, count))

def randomDiscard(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group.random()
    toDiscard(card, notifymute = True)
    rnd(1,10)
    notify("{} randomly discards {}.".format(me, card))

def mana(group, count = 1, x = 0, y = 0):
	mute()
	for i in range(0,count):
		if len(group) == 0: return
		card = group[0]
		toMana(card, notifymute = True)
		notify("{} charges top card of {} as mana.".format(me, group.name))
    
def endTurn(x = 0, y = 0):
    mute()
    notify("{} ends their turn.".format(me))
    
def shields(group, count = 1, conditional = False, x = 0, y = 0):
	mute()
	if conditional == True:
		maxCount = count
		count = askInteger("Set how many cards as shields? (Max = {})".format(maxCount), maxCount)
		if count == 0 or count > maxCount: return
	for card in group.top(count):
		if len(group) == 0: return
		card = group[0]
		toShields(card, notifymute = True)
		notify("{} sets top card of {} as shield.".format(me, group.name))

def search(group, count = 1, TypeFilter = "ALL" , CivFilter = "ALL", RaceFilter = "ALL", show = True, x = 0, y = 0):
	mute()
	if len(group) == 0: return
	for i in range(0,count):
		if TypeFilter != "ALL":
			cardsInGroup_Type_Filtered = [card for card in group if re.search(TypeFilter,card.Type)]
		else:
			cardsInGroup_Type_Filtered = [card for card in group]
		if CivFilter != "ALL":
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered if re.search(CivFilter,card.properties['Civilization'])]
		else:
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered]
		if RaceFilter != "ALL":
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered if re.search(RaceFilter,card.properties['Race'])]
		else:
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered]
		if len(cardsInGroup_CivTypeandRace_Filtered) == 0: return
		choice = askCard(cardsInGroup_CivTypeandRace_Filtered, 'Search card to take to hand (1 at a time)')
		if type(choice) is not Card: break
		toHand(choice, show)
	group.shuffle()
	notify("{} finishes searching his/her {}.".format(me, group.name))

def toMana(card, x = 0, y = 0, notifymute = False):
    mute()
    evolveDict = eval(me.getGlobalVariable('evolution'))
    if card._id in list(itertools.chain.from_iterable(evolveDict.values())):
        if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be placed into your mana zone.\nWould you like to override this?"):
            return
    if isMana(card):
        whisper("This is already mana")
        return
    card.moveToTable(0,0)
    card.orientation = Rot180
    if card._id in evolveDict:
        evolvedCardList = evolveDict[card._id]
        for evolvedCard in evolvedCardList:
            if Card(evolvedCard) in table:
                Card(evolvedCard).orientation = Rot180
        del evolveDict[card._id]
        me.setGlobalVariable('evolution', str(evolveDict))
    align()
    if notifymute == False:
        notify("{} charges {} as mana.".format(me, card))

def toShields(card, x = 0, y = 0, notifymute = False, alignCheck = True, ignoreEvo = False):
    mute()
    if isShield(card):
        whisper("This is already a shield.")
        return
    evolveDict = eval(me.getGlobalVariable('evolution'))
    if ignoreEvo == False and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
        if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be placed into your shield zone.\nWould you like to override this?"):
            return
    count = int(me.getGlobalVariable("shieldCount")) + 1
    me.setGlobalVariable("shieldCount", convertToString(count))
    if notifymute == False:
        if isCreature(card) or isMana(card):  ##If a visible card in play is turning into a shield, we want to record its name in the notify
            notify("{} sets {} as shield #{}.".format(me, card, count))
        else:
            notify("{} sets a card in {} as shield #{}.".format(me, card.group.name, count))
    card.moveToTable(0,0,True)
    if card.isFaceUp:
        card.isFaceUp = False
    if card.orientation != Rot0:
        card.orientation = Rot0
    card.markers[shieldMarker] = count
    if card._id in evolveDict:
        evolvedCardList = evolveDict[card._id]
        for evolvedCard in evolvedCardList:
            if Card(evolvedCard) in table:
                toShields(Card(evolvedCard), alignCheck = False, ignoreEvo = True)
        del evolveDict[card._id]
        me.setGlobalVariable('evolution', str(evolveDict))
    if alignCheck:
        align()
        
def toPlay(card, x = 0, y = 0, notifymute = False, evolveText = ''):
    mute()
    if card.Type == "Spell":
        if re.search("Charger", card.name):
            toMana(card)
        else:
            card.moveTo(card.owner.piles['Graveyard'])
    else:
        if re.search("Evolution", card.Type):
            targets = [c for c in table
                        if c.controller == me
                        and c.targetedBy
                        and c.targetedBy == me
                        and isCreature(c)]
            for c in targets:
                c.target(False) #remove the targets
            if len(targets) == 0:
                whisper("Cannot play card: You must target a creature to evolve first.")
                whisper("Hint: Shift-click a card to target it.")
                return
            else:
                targetList = [c._id for c in targets]
                evolveDict = eval(me.getGlobalVariable("evolution")) ##evolveDict tracks all cards 'underneath' the evolution creature
                for evolveTarget in targets: ##check to see if the evolution targets are also evolution creatures
                    if evolveTarget._id in evolveDict: ##if the card already has its own cards underneath it
                        if isCreature(evolveTarget):
                            targetList += evolveDict[evolveTarget._id] ##add those cards to the new evolution creature
                        del evolveDict[evolveTarget._id]
                evolveDict[card._id] = targetList
                me.setGlobalVariable("evolution", str(evolveDict))
                evolveText = ", evolving {}".format(", ".join([c.name for c in targets]))
        if card.group == table:
            card.moveTo(me.hand)
        card.moveToTable(0,0)
        if shieldMarker in card.markers:
            card.markers[shieldMarker] = 0
        align()
    if notifymute == False:
        notify("{} plays {}{}.".format(me, card, evolveText))
    if card.Type=='Spell':
        if card.name in onCast:
            exec(onCast[card.name])
    else:
        if card.name in onSummon:
            exec(onSummon[card.name])

def toDiscard(card, x = 0, y = 0, notifymute = False, alignCheck = True, ignoreEvo = False):
    mute()
    evolveDict = eval(me.getGlobalVariable('evolution'))
    if ignoreEvo == False and isCreature(card) and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
        if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be banished.\nWould you like to override this?"):
            return
    src = card.group
    card.moveTo(card.owner.piles['Graveyard'])
    if card._id in evolveDict:
        evolvedCardList = evolveDict[card._id]
        for evolvedCard in evolvedCardList:
            if Card(evolvedCard) in table:
                toDiscard(Card(evolvedCard), alignCheck = False, ignoreEvo = True)
        del evolveDict[card._id]
        me.setGlobalVariable('evolution', str(evolveDict))
    if notifymute == False:
        if src == table:
            notify("{} banishes {}.".format(me, card))
            if alignCheck:
                align()
        else:
            notify("{} discards {} from {}.".format(me, card, src.name))

def toHand(card, show = True, x = 0, y = 0, alignCheck = True, ignoreEvo = False):
	mute()
	src = card.group
	evolveDict = eval(me.getGlobalVariable('evolution'))
	if ignoreEvo == False and isCreature(card) and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
		if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be banished.\nWould you like to override this?"):
			return
	card.moveTo(card.owner.hand)
	if card._id in evolveDict:
		evolvedCardList = evolveDict[card._id]
		for evolvedCard in evolvedCardList:
			if Card(evolvedCard) in table:
				toHand(Card(evolvedCard), alignCheck = False, ignoreEvo = True)
		del evolveDict[card._id]
		me.setGlobalVariable('evolution', str(evolveDict))
	if show == True: 
		notify("{} moves {} to hand from {}.".format(card.owner, card, src.name))
	else:
		whisper("moved {} to hand from {}.".format(card, src.name))
	if alignCheck:
		align()

def toDeckTop(card, x = 0, y = 0):
    mute()
    toDeck(card)

def toDeckBottom(card, x = 0, y = 0):
    mute()
    toDeck(card, bottom = True)

def toDeck(card, bottom = False):
    mute()
    evolveDict = eval(me.getGlobalVariable('evolution'))
    if isCreature(card) and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
        if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be banished.\nWould you like to override this?"):
            return
    cardList = [card]
    if card._id in evolveDict:
        evolvedCardList = evolveDict[card._id]
        for evolvedCard in evolvedCardList:
            if Card(evolvedCard) in table:
                cardList.append(Card(evolvedCard))
        del evolveDict[card._id]
        me.setGlobalVariable('evolution', str(evolveDict))
    while len(cardList) > 0:
        if len(cardList) == 1:
            choice = 1
        else:
            choice = askChoice("Choose a card to place it on top of your deck.", [c.name for c in cardList])
        if choice > 0:
            c = cardList.pop(choice - 1)
            if bottom == True:
                notify("{} moves {} to bottom of Deck.".format(me, c))
                c.moveToBottom(c.owner.Deck)
            else:
                notify("{} moves {} to top of Deck.".format(me, c))
                c.moveTo(c.owner.Deck)
    align()