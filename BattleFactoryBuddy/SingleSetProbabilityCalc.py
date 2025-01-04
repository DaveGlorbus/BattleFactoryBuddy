import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import random
from time import perf_counter

def calcAllOccurences():
    setCount = len(StaticDataHandler.StaticDataHandler.getSetList())    
    resultArray = {}
    for set in StaticDataHandler.StaticDataHandler.getSetList():
        resultArray[set.id] = {}
        resultArray[set.id][0] = 1/setCount
        resultArray[set.id][1] = 0
        resultArray[set.id][2] = 0

    i = 1 
    while i < setCount +1:
        setA = StaticDataHandler.StaticDataHandler.getSetFromId(str(i))
        secondmonlist = []        
        j = 1
        validOptionsSecond = 0
        while j < setCount + 1:
            setB = StaticDataHandler.StaticDataHandler.getSetFromId(str(j))
            if setA.compatibilitycheck(setB):
                validOptionsSecond += 1
                secondmonlist.append(setB)
            j += 1
        for setB in secondmonlist:
            resultArray[setB.id][1] += 1/setCount/validOptionsSecond
            k = 1
            thirdmonlist = []
            validOptionsThird = 0
            while k < setCount + 1:
                setC = StaticDataHandler.StaticDataHandler.getSetFromId(str(k))
                if setA.compatibilitycheck(setC) and setB.compatibilitycheck(setC):
                    validOptionsThird += 1
                    thirdmonlist.append(setC)
                k += 1
            for setC in thirdmonlist:
                resultArray[setC.id][2] += 1/setCount/validOptionsSecond/validOptionsThird
        i += 1
        print("Done all " + setA.id + " teams")
    with open ("./BattleFactoryBuddy/Data/AllProbabilities.csv","w") as o:
        o.write("Set,Position 1,Position 2, Position 3,Total\n")
        for a in resultArray:
            o.write(",".join([a,str(resultArray[a][0]*100),str(resultArray[a][1]*100),str(resultArray[a][2]*100),str(resultArray[a][0]*100+resultArray[a][1]*100+resultArray[a][2]*100)])+ "\n")

if __name__ == "__main__":
    calcAllOccurences()
    
