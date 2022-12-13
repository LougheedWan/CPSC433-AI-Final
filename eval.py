import globalVariables
import random
from collections import Counter
def selectRule(population):
    print("Selecting Extension Rule..")

    if globalVariables.popMax > len(population):
        #select mutation or crossover
        selection = random.randint(0,1)
        if selection == 0:
            globalVariables.selection = "mutate"
        else:
            if len(population) < 2:
                globalVariables.selection = "mutate"
            else:
                globalVariables.selection = "cross"
    elif globalVariables.popMax <= len(population):
        globalVariables.selection = "delete"

def setEval(population):
    print("calculating Eval")
    gameArray = []
    practiceArray = []
    for schedule in population:
        gameMinEval = 0
        practiceMinEval = 0
        prefEval = 0
        pairEval = 0
        sectionEval = 0
        for element in schedule:
            #check to see if it is a game:
            if "PRC" not in element and "OPN" not in element:
                if element != "Eval" and element !="ID":
                    gameSlot = schedule[element]
                    #print("GAMESLOT: " + str(gameSlot))
                    gameArray.append(gameSlot)
                
            else:
                if element != "Eval" and element !="ID":
                    practiceSlot = schedule[element]
                    practiceArray.append(practiceSlot)
        #now check for gamemin
        dicOfGameTimes = dict(Counter(gameArray))
        print(dicOfGameTimes)
        #EDGE CASE, MISSING SLOTS BECAUSE NEVER ASSIGNED:
        if len(dicOfGameTimes) < len(globalVariables.gameSlots):
            for slots in globalVariables.gameSlots:
                if str(slots).strip() not in dicOfGameTimes:
                    print("ADDING 0 slot")
                    dicOfGameTimes.update({slots: 0})
        for times in dicOfGameTimes:
            difference = int(globalVariables.gameSlots[times]["gamemin"]) - dicOfGameTimes[times]
            print("DIFFERENCE: " + str(difference))
            if difference > 0:
                gameMinEval = gameMinEval + (difference * globalVariables.evalVariables["gamemin"])
                #print(gameMinEval)
        #now check for practicemin
        dicOfPracticeTimes = dict(Counter(practiceArray))
        if len(dicOfPracticeTimes) < len(globalVariables.practiceSlots):
            for slots in globalVariables.practiceSlots:
                if str(slots).strip() not in dicOfPracticeTimes:
                    dicOfPracticeTimes.update({slots: 0})
        for times in dicOfPracticeTimes:
            difference = int(globalVariables.practiceSlots[times]["practicemin"]) - dicOfPracticeTimes[times]
            if difference > 0:
                practiceMinEval = practiceMinEval + (difference * globalVariables.evalVariables["practicemin"])
        #reset gameArray and PracticeArray
        gameArray = []
        practiceArray = []    

        #check Preferences
        for preferences in globalVariables.preferences:
            splitString = str(preferences).split(", ")
            Id = splitString[2]
            timeInSchedule = schedule.get(Id)
            formatedString = splitString[0] + ", " + splitString[1]
            if str(timeInSchedule).strip() != formatedString:
                print("pref not achieved")
                prefEval = prefEval + int(splitString[3])
        
        #check Paired
        for pairs in globalVariables.pair:
            splitString = str(pairs).split(", ")
            ID1 = splitString[0]
            ID2 = splitString[1]
            slot1 = schedule.get(ID1)
            slot2 = schedule.get(ID2)
            print(slot1)
            print(slot2)
            if str(slot1).strip() != str(slot2).strip():
                print("Pair not achieved")
                pairEval = pairEval + globalVariables.evalVariables["notpaired"]
        #check section
        #YIANNI AND ISSAC CODE HERE
        #YOU ARE IN A FOR LOOP WITH THE VARIABLE schedule AS THE ACTIVE SCHEDULE YOU ARE WORKING ON, PLEASE UTILZE THIS VARIABE TO INSURE YOU ARE IN THE RIGHT SCHEDULE
        #UPDATE THE sectionEval VARIABLE WITH THE PROPER EVAL NUMBER AFTER EVAUATING THE ENTIRE POPULATION. sectionEval WILL REPRESENT THE EVAL NUMBER OF THIS SPECIFIC EVAL FUNCTION FOR schedule AND WILL AUTO ZERO OUT WHEN THE LOOP RESETS ONTO A NEW SCHEDULE
        #YOU ARE DONE ONCE YOU HAVE SUCCESSFULLY UPDATED sectionEval WITH THE PROPER INTEGER EVAL FUNCTION (FOR EACH SCHEDULE OF COURSE), I WILL DO THE REST OF THE WORK ON MONDAY
        #CHECK THE PROJECT PROBLEM FOR THE LOGIC NEEDED TO DO THIS EVAL FUNCTION (PG 6 AT THE BOTTOM). I AM THINKING IT IS ALONG THE LINES OF LOOPING THROUGH OUR SCHEDULE... THIS EVAL HAS NOTHING TO DO WITH THE INPUT TEXT FILE
        #THANK YOU!
        #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #BEGIN CODE HERE ENSURE YOU ARE ALIGNED WITH THE COMMENTS (PYTHON IS ALL ABOUT INDENTATION)
        #CHECK sectionEval
        sch_v = schedule.keys()
        # get all the keys in the schedule (league, age, div)
        already_check = []
        for v in sch_v: # loop through all keys
            for g in sch_v: # loop through all keys again
                # has to be a game
                if "PRC" not in v and "PRC" not in g:
                    if "OPN" not in v and "OPN" not in g:
                        sv = v.split()
                        sg = g.split()
                        if len(sg) > 1 and len(sv) > 1:
                            vv = sv[1]
                            gg = sg[1]
                            if v != g and vv == gg: # check to make sure we are not checking the same g/p
                                # if the time is the same and they have not already been checked
                                if str(schedule[v]) == str(schedule[g]) and v not in already_check and g not in already_check:
                                    print("Overlapping schedule found: " + v + " and " + g + " at " + schedule[v])
                                    sectionEval = sectionEval + globalVariables.evalVariables["section"]
                                    already_check.append(v)
                                    already_check.append(g)
        #CHECK sectionEval
        print("SECTION EVAL VARIABLE: " + str(sectionEval))

        #END CODE HERE
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #update Eval
        schedule["Eval"] = ((gameMinEval + practiceMinEval) * globalVariables.evalVariables["minfilled"]) + (prefEval * globalVariables.evalVariables["pref"]) + (pairEval * globalVariables.evalVariables["pair"]) + (sectionEval * globalVariables.evalVariables["secdiff"])

        #check for perfect answer
        if schedule["Eval"] == 0:
            #FOUND PEFECT ANSWER
            globalVariables.perfectAnswer = True
