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
            timeInSchedule = schedule[Id]
            formatedString = splitString[0] + ", " + splitString[1]
            if str(timeInSchedule).strip() != formatedString:
                print("pref not achieved")
                prefEval = prefEval + int(splitString[3])
        #update Eval
        schedule["Eval"] = ((gameMinEval + practiceMinEval) * globalVariables.evalVariables["minfilled"]) + (prefEval * globalVariables.evalVariables["pref"])
