#subfile to generate population for further analysis
#import statements:
import sys
import globalVariables
import random
import time

def parse_inputs():
    #print("Parsing inputs...")
    #read inputs and assign variables from cmd arguments
    globalVariables.evalVariables = {"minfilled": int(sys.argv[2]), "pref": int(sys.argv[3]), "pair": int(sys.argv[4]), "secdiff": int(sys.argv[5]), "gamemin": int(sys.argv[6]), "practicemin": int(sys.argv[7]), "notpaired": int(sys.argv[8]), "section": int(sys.argv[9])}

    #assign gameSlots to dictionary
    #print("opening input file: " + sys.argv[1])
    f = open(str(sys.argv[1]), "r")
    switch = ""
    for eachline in f:
        #print("line:" +eachline)
        if eachline.strip() == "Game slots:":
            #print("FOUND gameslots")
            switch = "gameSlots"
            continue
        elif eachline.strip() == "Practice slots:":
            #print("FOUND practiceslots")
            switch = "practiceSlots"
            continue
        elif eachline.strip() == "Games:":
            switch = "games"
            continue
        elif eachline.strip() == "Practices:":
            switch = "practices"
            continue
        elif eachline.strip() == "Not compatible:":
            switch  = "notCompatible"
            continue
        elif eachline.strip() == "Unwanted:":
            switch = "unwanted"
            continue
        elif eachline.strip() == "Preferences:":
            switch = "preferences"
            continue
        elif eachline.strip() == "Pair:":
            #print("FOUND Pair")
            switch = "pair"
            continue
        elif eachline.strip() == "Partial assignments:":
            switch = "partialAssignments"
            continue
        elif eachline.strip() == "":
            switch = ""

        if switch == "gameSlots":
            #print("IN GAMESLOTS")
            splitStr = eachline.strip().split(",")
            #print(splitStr)
            globalVariables.gameSlots.update({splitStr[0] + "," +splitStr[1]:{"gamemax":splitStr[2], "gamemin":splitStr[3]}})
        elif switch == "practiceSlots":
            splitStr = eachline.strip().split(",")
            globalVariables.practiceSlots.update({splitStr[0]+ "," +splitStr[1]:{"practicemax":splitStr[2], "practicemin":splitStr[3]}})
        elif switch == "games":
            globalVariables.games.append(eachline.strip())
        elif switch == "practices":
            globalVariables.practices.append(eachline.strip())
        elif switch == "notCompatible":
            globalVariables.notCompatible.append(eachline.strip())
        elif switch == "unwanted":
            globalVariables.unwanted.append(eachline.strip())
        elif switch == "preferences":
            globalVariables.preferences.append(eachline.strip())
        elif switch == "pair":
            globalVariables.pair.append(eachline.strip())
        elif switch == "partialAssignments":
            globalVariables.partialAssignments.append(eachline.strip())
    f.close()

def generate_pop():
    #TODO use parsed data and generate population
    print("Generating valid solutions...")
    timeout = time.time() + 5
    #start with partial assignments
    for partialAssignments in globalVariables.partialAssignments:
        splitString = str(partialAssignments).strip().split(", ")
        slot = str(splitString[1] + ", " + splitString[2])
        if "PRC" not in str(partialAssignments).strip():
            if slot in globalVariables.gameSlots:
                globalVariables.schedule.update({splitString[0]: slot})
                globalVariables.gameSlots[str(slot).strip()]["gamemax"] = int(globalVariables.gameSlots[str(slot).strip()]["gamemax"]) - 1
                globalVariables.games.remove(str(splitString[0]).strip())
            else:
                print("MALFORMED INPUTS IN PARTIAL ASSIGNMENT, EXITING ")
                exit()
        else:
            if slot in globalVariables.practiceSlots:
                globalVariables.schedule.update({splitString[0]: slot})
                globalVariables.practiceSlots[str(slot).strip()]["practicemax"] = int(globalVariables.practiceSlots[str(slot).strip()]["practicemax"]) - 1
                globalVariables.practices.remove(str(splitString[0]).strip())
            else:
                print("MALFORMED INPUTS IN PARTIAL ASSIGNMENT, EXITING ")
                exit()
    #choose a random game
    while(len(globalVariables.games) > 0):
        if time.time() > timeout:
            print("TIMEOUT REACHED, NO VALID SOLUTION FOUND, ABORTING")
            exit()
        print("choosing new game...")
        randomGame = random.choice(globalVariables.games)
        #choose a random gameSlot
        randomGameSlot = random.choice(list(globalVariables.gameSlots))
        tempAssignment = str(randomGame + ", " + randomGameSlot)
        #check hard constraints of assignment
        #check unwanted
        notValid = False
        notValid = checkUnwanted(tempAssignment)
        if notValid:
            continue
        #check notCompatible
        notValid = checkNotCompatible(randomGame, randomGameSlot)
        if notValid:
            continue
        #check for gamemax
        notValid = checkGameMax(randomGameSlot)
        if notValid:
            continue
        #check for evening
        notValid = checkEvening(randomGame, randomGameSlot)
        if notValid:
            continue
        #check for youth games overlap (games only)
        notValid = checkYouthOverlap(randomGame, randomGameSlot)
        if notValid:
            continue
        #check for tuesdays (games only)
        notValid = checkTuesdays(randomGameSlot)
        if notValid:
            continue
        #check for special booking
        notValid = checkSpecialBooking(randomGame, randomGameSlot)
        if notValid:
            continue
        if notValid == False:
            print("ALL CHECKS COMPLETED...ADDING GAME TO SCHEDULE")
            globalVariables.schedule.update({randomGame: randomGameSlot})
            #decrease gamemax
            globalVariables.gameSlots[str(randomGameSlot).strip()]["gamemax"] = int(globalVariables.gameSlots[str(randomGameSlot).strip()]["gamemax"]) - 1
            #print(globalVariables.gameSlots[str(randomGameSlot).strip()]["gamemax"])
            #remove game from game slots
            globalVariables.games.remove(str(randomGame).strip())
            #print(globalVariables.games)

    #now do the same thing for practices:
    while(len(globalVariables.practices) > 0):
        if time.time() > timeout:
            print("TIMEOUT REACHED, NO VALID SOLUTION FOUND, ABORTING")
            exit()
        print("choosing new practice...")
        randomPractice = random.choice(globalVariables.practices)
        #choose a random practice slot
        randomPracticeSlot = random.choice(list(globalVariables.practiceSlots))
        tempAssignment = str(randomPractice + ", " + randomPracticeSlot)
        #print(len(globalVariables.practices))
        #check hard constraints
        notValid = False
        notValid = checkUnwanted(tempAssignment)
        if notValid:
            continue
        notValid = checkNotCompatible(randomPractice, randomPracticeSlot)
        if notValid:
            continue
        notValid = checkPracticeMax(randomPracticeSlot)
        if notValid:
            continue
        notValid = checkEvening(randomPractice, randomPracticeSlot)
        if notValid:
            continue
        notValid = checkSpecialBooking(randomPractice, randomPracticeSlot)
        if notValid:
            continue
        if notValid == False:
            print("ALL CHECKS COMPLETED...ADDING PRACTICE TO SCHEDULE")
            globalVariables.schedule.update({randomPractice: randomPracticeSlot})
            #decrease practicemax
            globalVariables.practiceSlots[str(randomPracticeSlot).strip()]["practicemax"] = int(globalVariables.practiceSlots[str(randomPracticeSlot).strip()]["practicemax"]) - 1
            #remove practice from practice slots
            globalVariables.practices.remove(str(randomPractice).strip())
    #add in a blank eval value
    globalVariables.schedule.update({"Eval": 0})

    print("GENERATION COMPLETE...")
    #print(globalVariables.schedule)
    #check for hard constraints
    

def checkUnwanted(assignment):
    #print("CHECKING FOR UNWANTED")
    #print(assignment)
    for unwanted in globalVariables.unwanted:
        #print(str(unwanted).strip())
        if (str(unwanted).strip() == str(assignment).strip()):
            print("UNWANTED CONFLICT.. ABORTING")
            return True
    return False

def checkNotCompatible(game, slot):
    #print("CHECKING FOR NON COMPATIBLE")
    #print("CHOSEN GAME " + game)
    for notCompatible in globalVariables.notCompatible:
        stripped = str(notCompatible).strip().split(", ")
        if (stripped[0] == str(game).strip()):
            #print("Stripped[0]--" + stripped[0])
            #check to see if times conflict
            if stripped[1] in globalVariables.schedule:
                #print("In schedule, checking time")
                timeslot = globalVariables.schedule[stripped[1]]
            #print(timeslot)
                if (str(timeslot).strip() == str(slot).strip()):
                    print("NOT COMPATIBLE CONFLICT.. ABORTING")
                    return True
        if (stripped[1] == str(game).strip()):
            #print(stripped[1])
            #check to see if times conflict
            if stripped[0] in globalVariables.schedule:
                #print("In schedule, checking time")
                timeslot = globalVariables.schedule[stripped[0]]

                if (str(timeslot).strip() == str(slot).strip()):
                    print("NOT COMPATIBLE CONFLICT.. ABORTING")
                    return True

    return False

def checkGameMax(slot):
    #print("selected slot--" + slot)
    #print("CHECKING TO SEE IF GAMEMAX IS FULL")
    currentMax = globalVariables.gameSlots[str(slot).strip()]["gamemax"]
    print(currentMax)
    if int(currentMax)-1 < 0:
        print("GAMEMAX FULL ABORTING")
        return True
    return False

def checkPracticeMax(slot):
    currentMax = globalVariables.practiceSlots[str(slot).strip()]["practicemax"]
    #print(globalVariables.practiceSlots)
    if int(currentMax)-1 < 0:
        print("PRACTICEMAX FULL ABORTING")
        return True
    return False

def checkEvening(game, slot):
    if "DIV 09" in str(game).strip():
        if slot != "18;00" | slot != "19:00" | slot !="20:00":
            print("DIV 9 NOT IN EVENING, ABORTING")
            return True

        else:
            return False
    return False

#ONLY DO THIS CHECK IF YOU ARE MODIFYING GAMES, WE ASSUME WE KNOW THAT THE game PARAMETER IS A GAME AND NOT A PRACTICE 
def checkYouthOverlap(game, slot):
    splitString = str(game).strip().split(" ")
    tier = splitString[1]
    if ("U15" in tier) | ("U16" in tier) | ("U17" in tier) | ("U19" in tier):
        for element in globalVariables.schedule:
            #check to see if element is a youth division
            if ("U15" in str(element).strip()) | ("U16" in str(element).strip()) | ("U17" in str(element).strip()) | ("U19" in str(element).strip()):
                #check to see now if it is a practice
                if "PRC" in str(element).strip():
                    continue
                else:
                    if str(slot).strip() == str(globalVariables.schedule[element]):
                        print("YOUTH GAME TIERS OVERLAP ABORTING")
                        return True
    return False

def checkTuesdays(slot):
    if str(slot).strip() == "TU, 11:00":
        print("TUESDAY SLOT SELECTED, ABORTING")
        return True
    return False

def checkSpecialBooking(game, slot):
    if "CMSA U12T1S" in str(game).strip():
        if str(slot).strip() != "TU, 18:00":
            return True
        for element in globalVariables.schedule:
            if "CSMA U12T1" in str(element).strip():
                if str(slot).strip() == str(globalVariables.schedule[element]).strip:
                    print("SPECIAL BOOKING CONFLICT, ABORTING")
                    return True
    
    elif "CMSA U13T1S" in str(game).strip():
        if str(slot).strip() != "TU, 18:00":
            return True
        for element in globalVariables.schedule:
            if "CSMA U13T1" in str(element).strip():
                if str(slot).strip() == str(globalVariables.schedule[element]).strip:
                    print("SPECIAL BOOKING CONFLICT, ABORTING")
                    return True
    return False