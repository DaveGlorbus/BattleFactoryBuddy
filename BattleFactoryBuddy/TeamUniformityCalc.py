import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import random

# Script to generate all static data (teams and speed tiers) and save them off in CSV files. This allows us to precompute all available teams
# once and not have to do it per query (which would be prohibitively slow). These files are also large so aren't checked in
# and need to be generated per-checkout or if the underlying mon data changes.

# Spin through all combinations of 3 mons. For each combination see if they're a valid team. If they are, work out which phrase they go with.
# Once we've done that then write them into csvs using their uids for brevity.
def generateTeamList():    
    masterSetList = StaticDataHandler.StaticDataHandler.getSetList()

    # Initialise looking at sets 1, 2 and 3 and work from there.
    q = 0
    wakIds = StaticDataHandler.StaticDataHandler.getSpeciesFromName("Marowak").filter()
    waksightings = [0,0,0]
    laprasIds = StaticDataHandler.StaticDataHandler.getSpeciesFromName("Lapras").filter()
    laprasightings = [0,0,0]
    zardIds = StaticDataHandler.StaticDataHandler.getSpeciesFromName("Charizard").filter()
    zardsightings = [0,0,0]
    while q < 1000000:
        setList = masterSetList.copy()        
        random.shuffle(setList)       
        setA = setList.pop()
        setB = setList.pop()
        while not setA.compatibilitycheck(setB):
            setB = setList.pop()
        setC = setList.pop()
        while not setA.compatibilitycheck(setC) and setB.compatibilitycheck(setC):
            setC = setList.pop()
        if setA.uid in wakIds:
            waksightings[0] += 1
        elif setB.uid in wakIds:
            waksightings[1] += 1
        elif setC.uid in wakIds:
            waksightings[2] += 1
        if setA.uid in laprasIds:
            laprasightings[0] += 1
        elif setB.uid in laprasIds:
            laprasightings[1] += 1
        elif setC.uid in laprasIds:
            laprasightings[2] += 1
        if setA.uid in zardIds:
            zardsightings[0] += 1
        elif setB.uid in zardIds:
            zardsightings[1] += 1
        elif setC.uid in zardIds:
            zardsightings[2] += 1
        q += 1
        if q%100000 == 0:
            print("Done " + str(q))
    print("Wak - " + str(waksightings))
    print("Lapras - " + str(laprasightings))
    print("Zard - " + str(zardsightings))

if __name__ == "__main__":
    generateTeamList()

        