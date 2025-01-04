import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import random
from time import perf_counter

def calcSetOccurences(setName):
    ourSet = StaticDataHandler.StaticDataHandler.getSetFromName(setName)
    resultArray = []
    setCount = len(StaticDataHandler.StaticDataHandler.getSetList())
    # Calc slot 1 odds
    resultArray.append(1/setCount)

    # Calc slot 2 odds for vaporeon-4
    runningProbability = float(0)
    i = 1 
    while i < setCount:
        setA = StaticDataHandler.StaticDataHandler.getSetFromId(str(i))
        if ourSet.compatibilitycheck(setA):
            j = 1
            validOptions = 0
            while j < setCount:
                if setA.compatibilitycheck(StaticDataHandler.StaticDataHandler.getSetFromId(str(j))):
                    validOptions += 1
                j += 1
            # We'll have caught our set here.
            print(",".join([setA.id,str(validOptions)]))
            runningProbability += 1/setCount/(validOptions)            
        else:
            print(",".join([setA.id,"Invalid"]))
        i += 1
    print(runningProbability*100)

if __name__ == "__main__":
    calcSetOccurences("Vaporeon-4")
