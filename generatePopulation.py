#subfile to generate population for further analysis
#import statements:
import sys
import globalVariables


def parse_inputs():
    print("Parsing inputs...")
    #read inputs and assign variables from cmd arguments
    globalVariables.evalVariables = {"minfilled": int(sys.argv[2]), "pref": int(sys.argv[3]), "pair": int(sys.argv[4]), "secdiff": int(sys.argv[5]), "gamemin": int(sys.argv[6]), "practicemin": int(sys.argv[7]), "notpaired": int(sys.argv[8]), "section": int(sys.argv[9])}

    #assign gameSlots to dictionary
    print("opening input file: " + sys.argv[1])
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
        elif eachline.strip() == "Practices":
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
            globalVariables.gameSlots.update({splitStr[0]+splitStr[1]:{"gamemax":splitStr[2], "gamemin":splitStr[3]}})
        elif switch == "practiceSlots":
            splitStr = eachline.strip().split(",")
            globalVariables.practiceSlots.update({splitStr[0]+splitStr[1]:{"practicemax":splitStr[2], "practicemin":splitStr[3]}})
        elif switch == "games":
            globalVariables.games.append(eachline.strip())
        elif switch == "pratices":
            globalVariables.practices.append(eachline.strip())
        elif switch == "notCompatible":
            globalVariables.notCompatible.append(eachline.strip())
        elif switch == "unwanted":
            splitStr = eachline.strip().split(",")
            globalVariables.unwanted.update({splitStr[0] : (splitStr[1]+ splitStr[2])})
        elif switch == "preferences":
            splitStr = eachline.strip().split(",")
            globalVariables.preferences.update({splitStr[0]+splitStr[1]: {"ID": splitStr[2], "prefValue": splitStr[3]}})
        elif switch == "pair":
            globalVariables.pair.append(eachline.strip())
        elif switch == "partialAssignments":
            splitStr = eachline.strip().split(",")
            globalVariables.partialAssignments.update({splitStr[0]: (splitStr[1]+splitStr[2])})
    f.close()

def generate_pop():
    #TODO use parsed data and generate population
    print("Generating valid solutions...")