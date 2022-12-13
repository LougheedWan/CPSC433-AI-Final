import generatePopulation
import globalVariables
import math
import random

def mutate (currentPop):

    population = currentPop
    popNum = len(population)
    popMax = globalVariables.popMax
    
    # mutateNum is the number of facts in the population that will be mutated
    mutateNum = random.randint(1, (popMax - popNum))

    for i in range(mutateNum):
    
        #select a random game/practice
        randomFact = random.choice(globalVariables.games + globalVariables.practices)
        #select a random time slot
        randomSlot = random.choice(list(globalVariables.gameSlots) + list(globalVariables.practiceSlots))
    
        notCompatible = False
        maxReach = False
        #check notCompatible
        notCompatible = generatePopulation.checkNotCompatible(randomFact, randomSlot)
        #check for max 
        if randomSlot in globalVariables.practiceSlots:
            maxReach = generatePopulation.checkPracticeMax(randomSlot)
        else: 
            maxReach = generatePopulation.checkGameMax(randomSlot)
    
        if notCompatible == False & maxReach == False:
            globalVariables.schedule.update({randomFact: randomSlot})
            #decrease gamemax or practicemax
            if randomSlot in globalVariables.practiceSlots:
                globalVariables.practiceSlots[str(randomSlot).strip()]["practicemax"] = int(globalVariables.practiceSlots[str(randomSlot).strip()]["practicemax"]) - 1
            else:
                globalVariables.gameSlots[str(randomSlot).strip()]["gamemax"] = int(globalVariables.gameSlots[str(randomSlot).strip()]["gamemax"]) - 1
    
    return population

