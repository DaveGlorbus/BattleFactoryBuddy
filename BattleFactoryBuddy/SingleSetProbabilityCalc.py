import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import BattleFactoryBuddy.Team as Team
import random
from time import perf_counter

def calcAllOccurences():
    setCount = len(StaticDataHandler.StaticDataHandler.getSetList())    
    resultArray = {}
    for set in StaticDataHandler.StaticDataHandler.getSetList():
        for settype in set.types:
            if settype not in resultArray:                
                resultArray[settype] = {}
                i = 0
                while i < 9:
                    resultArray[settype][i] = {}
                    resultArray[settype][i]["total"] = 0
                    i+=1
    resultArray["None"] = {}
    i = 0
    while i < 9:
        resultArray["None"][i] = {}
        resultArray["None"][i]["total"] = 0
        i+=1
        
    for set in StaticDataHandler.StaticDataHandler.getSetList():
        for t in resultArray:
            for s in resultArray[t]:                
                resultArray[t][s][set.id] = {}
                resultArray[t][s][set.id][0] = 0
                resultArray[t][s][set.id][1] = 0
                resultArray[t][s][set.id][2] = 0
    print("Set up result dictionaries")
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
            #print("Considering all " + setA.id + " and " + setB.id + " teams")         
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
                team = Team.Team(setA,setB,setC) 
                resultArray[team.type][team.style]["total"] += 1/setCount/validOptionsSecond/validOptionsThird                  
                resultArray[team.type][team.style][setA.id][0] += 1/setCount/validOptionsSecond/validOptionsThird
                resultArray[team.type][team.style][setB.id][1] += 1/setCount/validOptionsSecond/validOptionsThird
                resultArray[team.type][team.style][setC.id][2] += 1/setCount/validOptionsSecond/validOptionsThird
        i += 1
        print("Done all " + setA.id + " teams")
    for type in resultArray:
        for style in resultArray[type]:
            with open ("./BattleFactoryBuddy/Data/ProceduralProbs/"+type+"-"+str(style)+".csv","w") as o:
                o.write("Set,Position 1,Position 2, Position 3,Total\n")
                for setId in resultArray[type][style]:
                    if setId == "total" or resultArray[type][style]["total"] == 0:
                        continue
                    pos1odds = 100*resultArray[type][style][setId][0]/resultArray[type][style]["total"]
                    pos2odds = 100*resultArray[type][style][setId][1]/resultArray[type][style]["total"]
                    pos3odds = 100*resultArray[type][style][setId][2]/resultArray[type][style]["total"]
                    totalodds = pos1odds + pos2odds + pos3odds
                    o.write(",".join([setId,str(pos1odds)+"%",str(pos2odds)+"%",str(pos3odds)+"%",str(totalodds)+"%"])+ "\n")

if __name__ == "__main__":
    calcAllOccurences()
    

