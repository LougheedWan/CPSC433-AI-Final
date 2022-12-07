# implements the operations of the mutation extension rule

import generatePopulation
import globalVariables
import math
import random

def mutation (currentPop):

    population = currentPop
    popNum = len(population)
    popMax = 1000
    
    # mutateNum is the number of facts in the population that will be mutated
    mutateNum = random.randrange(1, (popMax - popNum))

for i in mutateNum:
    
    randomFact = random.choice(population.games + population.practices)
    randomSlot = random.choice(list(population.gameSlots) + list(population.practiceSlots))
    
    notCompatible = False
    maxReach = False
    #check notCompatible
    notCompatible = checkNotCompatible(randomFact, randomSlot)
    #check for max 
    maxReach = checkMax(randomSlot)
    
    if notCompatible == False & maxReach == False:
        population.schedule.update({randomFact: randomSlot})
        #decrease gamemax or practicemax
      
    
