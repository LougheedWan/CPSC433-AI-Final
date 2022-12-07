
# call crossover.cross(population) to append fk and fg to the pop
import globalVariables
import generatePopulation
import random

def cross(populationOrig):
    population = populationOrig
    id = population[len(population) - 1]["ID"] + 1
    
    # sort the population of schedules from lowest fitness value to highest
    sort_(population)
    
    # fi has a random schedule from the top 30%
    length30 = round(0.3 * len(population))
    fi = population[random.randint(0, length30)] 
    # fj has a random schedule from the whole population
    fj = population[random.randint(0, len(population) - 1)]
    fk = {}
    fg = {}
    # key is the game/practice 
    # .get(x) is the slot

    # if a game/practice has already been scheduled then we will ignore 
    # it on a first come first serve basis
    k = fi.keys()    
    for x in k:
        if "MO" or "FR" in fi.get(x):
            if check_scheduling(x, fi.get(x), fk):
                fk[x] = fi.get(x)
        if "TU" or "THUR" in fi.get(x):
            if check_scheduling(x, fi.get(x), fg):
                fg[x] = fi.get(x)
    k = fj.keys()
    for x in k:
        if "MO" or "FR" in fj.get(x):
            if check_scheduling(x, fi.get(x), fg):
                fg[x] = fi.get(x)
        if "TU" or "THUR" in fj.get(x):
            if check_scheduling(x, fi.get(x), fk):
                fk[x] = fi.get(x)

    fk["ID"] = id 
    fg["ID"] = id + 1
    # append to the end of the current population
    # update their IDs
    population.append(fk)
    population.append(fg)

 # fg and fk are the two child dictionaries that will be added to the end of the population
 
# checks the constraints that can be broken by the new schedules
# also check if the game or practice has already been scheduled and if
# it has then we sort by first come first serve
def check_scheduling(gp, slot, population):
    valid = True
    valid = not generatePopulation.checkNotCompatible(gp, slot)
    if valid:
        valid = not generatePopulation.checkUnwanted(str(str(gp) + ", " + str(slot)))
    if valid:
        valid = not scheduled(population, gp)
    if valid:
        valid = not generatePopulation.checkSpecialBooking(gp, slot)
    if valid:
        valid = not generatePopulation.checkEvening(gp, slot)
    return valid

def scheduled(population, pg):
    return pg in population.values()

# sort the population from lowest fitness value to highest 
def sort_(population):    
    if(len(population) > 1):
        mid = len(population)//2
        sub1 = population[:mid]
        sub2 = population[mid:]
        sort_(sub1)
        sort_(sub2)
        i = j = k = 0
        while i < len(sub1) and j < len(sub2): 
            if sub1[i].get("Eval") < sub2[j].get("Eval"):
                population[k] = sub1[i]
                i += 1
            else:
                population[k] = sub2[j]
                j += 1  
            k += 1
        while i < len(sub1):
            population[k] = sub1[i]
            i += 1
            k += 1
        while j < len(sub2):
            population[k] = sub2[j]
            j += 1
            k += 1