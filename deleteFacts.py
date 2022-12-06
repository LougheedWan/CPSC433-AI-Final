# implements the operations of the deletion extension rule
# deletion essentially deletes individual facts/schedules from a population when the current number of facts exceeds the maximum number of facts allowed in a single population
# a single run of this operation deletes about 20% of the facts from the population

from operator import itemgetter
import globalVariables
import math
import random

def delete(currentpop):
    population = currentpop

    # step 1. rank the facts based on their eval-value from the highest to the lowest (i.e., least fit to the fittest)
    eval_sorted_pop = sorted(population, key=itemgetter('Eval'), reverse=True)
    popnum = len(population)

    # step 2. from a pool of the least fit 40%, randomly select 50% of the facts to delete
    poolnum = math.ceil(popnum * 0.4)
    delete_pool = eval_sorted_pop[0:poolnum]
    # deletenum is the number of facts that will be deleted
    deletenum = math.ceil(poolnum/2)
    
    # delete contains the facts that will be deleted 
    delete = random.sample(delete_pool, deletenum)
    # loop: if the [identifier] = one of the list of numbers sampled, delete from population
    delete_id = []
    for fact in delete:
        delete_id.append(fact['ID'])
    
    for fact in population:
        id_val = fact['ID']
        if(id_val in delete_id):
            population.remove(fact)
    
    return population