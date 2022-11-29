#Main execution file: Run system off this file:
#To run program: type "python main.py"
import generatePopulation
import globalVariables

print("Intiating Algorithm")

#TODO: Generate our population: Input: textfile and integer inputs; Output: population of N valid schedules (Lougheed)
generatePopulation.parse_inputs()
print(globalVariables.pair)
generatePopulation.generate_pop()

#Example output format: output = {"CSMA U13T3 DIV 01": "MO, 10:00", "CSMA U13T3 DIV 01 PRC 01": "TU, 10:00" .... "EVAL": 30}
#We use a dictonary to store ONE valid schedule, our populaton will be an array of n length of these dictonaries.
#NOTE: all data is now inputed into different data structures defined in globalVariables.py, this should help with the Evaluation of best solutions.
#All functions below should take ONE valid schedule at a time, and we shall repeat the functions for all schedules

#TODO: Deletion (Alexis)

#TODO: Mutation (Issac)

#TODO: Crossover (Yianni)

#TODO: Evaluate best solutions and repeat, this TODO also includes determining which schedules to apply the extention rules to. (Chirag)