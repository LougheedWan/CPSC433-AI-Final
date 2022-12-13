import generatePopulation
import globalVariables
import math
import random

def mutate (currentPop):
    print("STARTING MUTATION...")

    population  = currentPop
    print("PRINTING THE BEFORE POPULATION...\n", population)
    popNum = len(population)
    popMax = globalVariables.popMax
    
    # step 1. select facts to mutate from the population
    # mutateNum is the number of facts in the population that will be mutated
    mutateNum = random.randint(1, popNum)
    print("MUTATENUM: ", mutateNum)

    #mutateNum = 1

    # mutatePop contains the facts that will be mutated
    mutatePop = random.sample(population, mutateNum)
    print("MUTATEPOP...\n", mutatePop)

    id = int(popNum) + 1

    for schedule in mutatePop: 
        # step 2. mutate a game in the schedule 
        # randomly select a game or a practice to mutate 
        keyVal = key, val = random.choice(list(schedule.items()))    # keyVal is a tuple e.g., ('CMSA U17T1 DIV 01', 'MO, 9:00')

        # make sure the keyVal is not eval or ID
        while((keyVal[0].find('Eval') != -1) or (keyVal[0].find('ID') != -1)):
            keyVal = key, val = random.choice(list(schedule.items()))
        
        # partial assignments should not be mutated
        PartialAssign = partialAssignCheck(keyVal[0])
        while((PartialAssign == True)):
            keyVal = key, val = random.choice(list(schedule.items()))
            # keep generating a new pair until it's not a partial assignment one
            while((keyVal[0].find('Eval') != -1) or (keyVal[0].find('ID') != -1)):
                # have to check for the not eval or ID condition again 
                keyVal = key, val = random.choice(list(schedule.items()))
            PartialAssign = partialAssignCheck(keyVal[0])

        # figure out if the selected tuple contains a game or a practice
        if((keyVal[0].find('PRC') == -1) and (keyVal[0].find('OPN') == -1)):
            # selected a game 
            mutateGame = keyVal[0]
            oldGameSlot = keyVal[1]
            #TODO: decrease the gamemax value of oldGameSlot 
            print("mutateGame: ", mutateGame)

            # randomly select a new game slot to assign mutateGame to
            newKeyVal = key, val = random.choice(list(schedule.items()))
            newTempGameSlot = newKeyVal[1]
            print("newTempGameSlot ", newTempGameSlot)
            
            isSameSlot = True
            isGameSlot = False

            MaxExceed = True
            Unwanted = True
            NotCompatible = True

            isEvening = True
            YouthOverlap = True
            chkTues = True
            chkSpecBooking = True

            firstIter = True
            while((isSameSlot == True) or (isGameSlot == False) or (MaxExceed == True) or (Unwanted == True) or (NotCompatible == True) or (isEvening == True) or (YouthOverlap == True) or (chkTues == True) or (chkSpecBooking == True)):
                newKeyVal = key, val = random.choice(list(schedule.items()))
                newTempGameSlot = newKeyVal[1]
                print("newTempGameSlot AGAIN: ", newTempGameSlot)
                    
                firstIter = False
                
                # make sure the same slot is not chosen
                if(newTempGameSlot == oldGameSlot):
                    print("same slot chosen")
                    continue
                else:
                    print("same slot not chosen")
                    isSameSlot = False

                # make sure the new slot is a game slot 
                chkGameSlot = checkGameSlot(newTempGameSlot)
                if(chkGameSlot == False):
                    print("not a game slot")
                    continue
                else:
                    isGameSlot = True
                    print("game slot")

                # make sure the selected slot does not exceed gamemax
                MaxEx = generatePopulation.checkGameMax(newTempGameSlot)
                if(MaxEx == True):
                    print("gamemax slot: go again")
                    continue
                else:
                    MaxExceed = False
                    print("gamemax not exceeded")
                
                # make sure the game is not in an unwanted slot 
                tempAssignment = str(mutateGame + "," + newTempGameSlot)
                if(generatePopulation.checkUnwanted(tempAssignment) == True):
                    print("unwanted failed: go again")
                    continue
                else:
                    print("unwanted check passed")
                    Unwanted = False
                
                # check for the not compatible hard constraint
                if(generatePopulation.checkNotCompatible(mutateGame, newTempGameSlot) == True):
                    print("not compatible failed: go again")
                    continue
                else:
                    print("not compatible check passed")
                    NotCompatible = False
                    print(isSameSlot, isGameSlot, MaxExceed, Unwanted, NotCompatible)

                # evening check
                if(generatePopulation.checkEvening(mutateGame, newTempGameSlot)):
                    print("evening check failed")
                    continue
                else:
                    print("evening check passed")
                    isEvening = False
                
                # youth games check
                if(generatePopulation.checkYouthOverlap(mutateGame, newTempGameSlot)):
                    print("youth overlap check failed")
                    continue
                else:
                    print("youth overlap check passed")
                    YouthOverlap = False

                # Tuesday check
                if(generatePopulation.checkTuesdays(newTempGameSlot)):
                    print("Tues check failed")
                    continue
                else:
                    print("Tues check passed")
                    chkTues = False  
                
                # Special bookings check
                if(generatePopulation.checkSpecialBooking(mutateGame, newTempGameSlot)):
                    print("spec booking check failed")
                    continue
                else:
                    print("spec booking check passed")
                    chkSpecBooking = False

            newGameSlot = newTempGameSlot
            #TODO: increase the practicemax value of newPrcSlot 
            
            # update the schedule with the mutated pair 
            schedule.update({mutateGame: newGameSlot})
            tempSchedule = schedule
            tempSchedule["ID"] = id
            # give this new schedule a new ID
            #schedule["ID"] = id

            print("NEWSCHED GAME MUTATED:\n", schedule)   

        else:
            # selected a practice  
            mutatePrc = keyVal[0]
            oldPrcSlot = keyVal[1]
            #TODO: decrease the practicemax value of oldPrcSlot 
            print("mutatePrc: ", mutatePrc)

            # randomly select a new practice slot to assign mutatePrc to
            newKeyVal = key, val = random.choice(list(schedule.items()))
            newTempPrcSlot = newKeyVal[1]
            print("newTempPrcSlot ", newTempPrcSlot)
            
            isSameSlot = True
            isPrcSlot = False

            MaxExceed = True
            Unwanted = True
            NotCompatible = True

            isEvening = True
            chkSpecBooking = True

            firstIter = True
            while((isSameSlot == True) or (isPrcSlot == False) or (MaxExceed == True) or (Unwanted == True) or (NotCompatible == True) or
                 (isEvening == True) or (chkSpecBooking == True)):
                if(firstIter == False):
                    newKeyVal = key, val = random.choice(list(schedule.items()))
                    newTempPrcSlot = newKeyVal[1]
                    print("newTempPrcSlot AGAIN: ", newTempPrcSlot)
                
                firstIter = False
                
                # make sure the same slot is not chosen
                if(newTempPrcSlot == oldPrcSlot):
                    print("same slot chosen")
                    continue
                else:
                    print("same slot not chosen")
                    isSameSlot = False

                # make sure the new slot is a practice slot 
                chkPrcSlot = checkPrcSlot(newTempPrcSlot)
                if(chkPrcSlot == False):
                    print("not a practice slot")
                    continue
                else:
                    isPrcSlot = True
                    print("practice slot")

                # make sure the selected slot does not exceed practicemax
                MaxEx = generatePopulation.checkPracticeMax(newTempPrcSlot)
                if(MaxEx == True):
                    print("practicemax slot: go again")
                    continue
                else:
                    MaxExceed = False
                    print("practicemax not exceeded")
                
                # make sure the practice is not in an unwanted slot 
                tempAssignment = str(mutatePrc + "," + newTempPrcSlot)
                if(generatePopulation.checkUnwanted(tempAssignment) == True):
                    print("unwanted failed: go again")
                    continue
                else:
                    print("unwanted check passed")
                    Unwanted = False
                
                # check for the not compatible hard constraint
                if(generatePopulation.checkNotCompatible(mutatePrc, newTempPrcSlot) == True):
                    print("not compatible failed: go again")
                    continue
                else:
                    print("not compatible check passed")
                    NotCompatible = False
                    print(isSameSlot, isPrcSlot, MaxExceed, Unwanted, NotCompatible)
                
                # evening check
                if(generatePopulation.checkEvening(mutatePrc, newTempPrcSlot)):
                    print("evening check failed")
                    continue
                else:
                    print("evening check passed")
                    isEvening = False
                
                # special bookings check
                if(generatePopulation.checkSpecialBooking(mutatePrc, newTempPrcSlot)):
                    print("special booking check failed")
                    continue
                else:
                    print("special booking check passed")
                    chkSpecBooking = False
                

            newPrcSlot = newTempPrcSlot
            #TODO: increase the practicemax value of newPrcSlot
            # update the schedule with the mutated pair 
            schedule.update({mutatePrc: newPrcSlot})   
            tempSchedule = schedule
            tempSchedule["ID"] = id
            # give this new schedule a new ID
            #schedule["ID"] = id

            print("NEWSCHED PRACTICE MUTATED:\n", schedule)
        
        population.append(tempSchedule)

        id = id + 1
    
    print("MUTATION DONE")
    print("NEW POPULATION:\n", population)
    return population 


# check if the selected pair is a partial assignment
def partialAssignCheck(pair):
    for partialAssignments in globalVariables.partialAssignments:
        splitString = str(partialAssignments).strip().split(", ")
        GameOrPrc = str(splitString[0])
        if(pair == GameOrPrc):
            return True
    return False 


# check if the new slot is a game slot 
def checkGameSlot(TempGameSlot):
    for gameSlot in globalVariables.gameSlots:
        print(gameSlot)
        print("TEMPGAMESLOT ", TempGameSlot)
        if(TempGameSlot == gameSlot):
            return True 
    return False               

# check if the new slot is a practice slot 
def checkPrcSlot(TempPrcSlot):
    for PrcSlot in globalVariables.practiceSlots:
        print(PrcSlot)
        print("TEMPPRCSLOT ", TempPrcSlot)
        if(TempPrcSlot == PrcSlot):
            return True 
    return False               
             