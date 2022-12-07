#Main execution file: Run system off this file:
#To run program: type "python main.py"
import generatePopulation
import globalVariables
import deleteFacts

print("Intiating Algorithm")

#TODO: Generate our population: Input: textfile and integer inputs; Output: population of N valid schedules (Lougheed)
#lets generate 4 schedules first..
# using this number as popnum to keep track of the number of facts in a population would be convenient
for x in range(4):
    generatePopulation.parse_inputs()
    #print(globalVariables.games)
    generatePopulation.generate_pop()

    # add an identifier value for the schedule 
    globalVariables.schedule.update({"ID": x})

    globalVariables.population.append(globalVariables.schedule)
    #reset
    globalVariables.schedule = {}
    globalVariables.partialAssignments = []
    globalVariables.pair = []
    globalVariables.preferences = []
    globalVariables.unwanted = []
    globalVariables.notCompatible = []
    globalVariables.practices = []
    globalVariables.games = []
    globalVariables.practiceSlots = {}
    globalVariables.gameSlots = {}
    globalVariables.evalVariables = {}
    
#final parse to reset back to original data
generatePopulation.parse_inputs()
print(globalVariables.population)
#Example output format: output = {"CSMA U13T3 DIV 01": "MO, 10:00", "CSMA U13T3 DIV 01 PRC 01": "TU, 10:00" .... "EVAL": 30}
#We use a dictonary to store ONE valid schedule, our population will be an array of n length of these dictonaries.
#NOTE: all data is now inputted into different data structures defined in globalVariables.py, this should help with the Evaluation of best solutions.
#All functions below should take ONE valid schedule at a time, and we shall repeat the functions for all schedules

#TODO: Deletion (Alexis)
population = deleteFacts.delete(globalVariables.population)
#print("Testing the deletion operation...")
#print(population)

#TODO: Mutation (Isaac)
population = mutation.mutate(globalVariables.population)
#TODO: Crossover (Yianni)

#TODO: (Chirag) Evaluate best solutions and repeat, this TODO also includes:
# 1. determing which class of extension rules to choose (section 2.3.1 f_wert in the paper)
# do not worry about choosing what individuals (i..e, schedules) to apply the extension rules to - this should be implemented above, unique for each rule.

# 2. termination: think about it like this - each operation (deletion, mutation or crossover) will generate a new population of schedules. Each new population equates to a new generation. 
# Create a static variable for the number of generations (e.g., generationNum = 20). Once this number of generations is reached, terminate.

