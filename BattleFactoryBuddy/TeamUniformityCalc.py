import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import random
from time import perf_counter

# Script to generate all static data (teams and speed tiers) and save them off in CSV files. This allows us to precompute all available teams
# once and not have to do it per query (which would be prohibitively slow). These files are also large so aren't checked in
# and need to be generated per-checkout or if the underlying mon data changes.

# Spin through all combinations of 3 mons. For each combination see if they're a valid team. If they are, work out which phrase they go with.
# Once we've done that then write them into csvs using their uids for brevity.
def generateTeamList():    
    masterSetListLen = len(StaticDataHandler.StaticDataHandler.getSetList())

    # Initialise looking at sets 1, 2 and 3 and work from there.
    q = 0
    results = {}
    for set in StaticDataHandler.StaticDataHandler.getSetList():
        if set.id not in results:            
            results[set.id] = {}
            results[set.id][0] = 0
            results[set.id][1] = 0
            results[set.id][2] = 0
    t1_start = perf_counter() 
    while q < 100000000:        
        setA = StaticDataHandler.StaticDataHandler.getSetFromId(str(random.randint(1,masterSetListLen)))
        setB = StaticDataHandler.StaticDataHandler.getSetFromId(str(random.randint(1,masterSetListLen)))
        while not setA.compatibilitycheck(setB):
            setB = StaticDataHandler.StaticDataHandler.getSetFromId(str(random.randint(1,masterSetListLen)))
        setC = StaticDataHandler.StaticDataHandler.getSetFromId(str(random.randint(1,masterSetListLen)))
        while not setA.compatibilitycheck(setC) and setB.compatibilitycheck(setC):
            setC = StaticDataHandler.StaticDataHandler.getSetFromId(str(random.randint(1,masterSetListLen)))
        results[setA.id][0] = results[setA.id][0] + 1
        results[setB.id][1] = results[setB.id][1] + 1
        results[setC.id][2] = results[setC.id][2] + 1
        q += 1
        if q%1000000 == 0:
            t1_stop = perf_counter() 
            print("Done " + str(q/1000000) + "M. Last 1M in " + str(t1_stop - t1_start))
            t1_start = t1_stop
    for setid in results:
        print(",".join([setid, str(results[setid][0]),str(results[setid][1]),str(results[setid][2])]))

if __name__ == "__main__":
    generateTeamList()

        