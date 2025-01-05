import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import BattleFactoryBuddy.Team as Team
import BattleFactoryBuddy.StaticTeamUtils as StaticTeamUtils
import random
from time import perf_counter
from pathlib import Path

# RUN THIS USING calcSetOdds.bat
# Alter the fixed mons by changing the lockspecies
# Create a directory called 

def calcAllOccurences(inputdict):    
    validOptionsFirst = len(StaticDataHandler.StaticDataHandler.getSetList())    
    # CREATE RESULTS ARRAY
    resultArray = {}    
    resultArray["total"] = 0
    for set in StaticDataHandler.StaticDataHandler.getSetList():
        resultArray[set.id] = {}
        resultArray[set.id][0] = 0
        resultArray[set.id][1] = 0
        resultArray[set.id][2] = 0

    # SET UP LIST OF MONS VALID FOR THESE TEAMS
    blockedSpecies = [inputdict["Team1"],inputdict["Team2"],inputdict["Team3"],inputdict["LastOpp1"],inputdict["LastOpp2"],inputdict["LastOpp3"]]
    while "" in blockedSpecies:
        blockedSpecies.remove("")
    setList = []
    firstSetList = []
    for set in StaticDataHandler.StaticDataHandler.getSetList():
        # !TODO - Add round / level logic
        if (not True):
            continue        
        if set.speciesName in blockedSpecies:
            continue
        resultArray[set.id] = {}
        resultArray[set.id][0] = 0
        resultArray[set.id][1] = 0
        resultArray[set.id][2] = 0
        if inputdict["Species1"] != "":
            if inputdict["Species1"] == set.speciesName:
                firstSetList.append(set)
            else:
                setList.append(set)
        else:
            setList.append(set)
    if firstSetList == []:
        firstSetList = setList
    validOptionsFirst = len(firstSetList)    

    for setA in firstSetList:        
        secondmonlist = []                
        validOptionsSecond = 0
        for setB in setList:            
            if setA.compatibilitycheck(setB):
                validOptionsSecond += 1
                secondmonlist.append(setB)            
        for setB in secondmonlist:                           
            thirdmonlist = []
            validOptionsThird = 0
            for setC in setList:
                if setA.compatibilitycheck(setC) and setB.compatibilitycheck(setC):
                    validOptionsThird += 1
                    thirdmonlist.append(setC)                
            for setC in thirdmonlist:
                # TEAM VALIDATION - cover species 2 and species 3 if they're here.
                if inputdict["Species2"] != "" and setB.speciesName != inputdict["Species2"] and setC.speciesName != inputdict["Species2"]:
                    continue
                if inputdict["Species3"] != "" and setB.speciesName != inputdict["Species3"] and setC.speciesName != inputdict["Species3"]:
                    continue
                (teamType, teamStyle) = StaticTeamUtils.StaticTeamUtils.getTeamInfo(setA,setB,setC)                 
                if teamType != inputdict["Type"] or str(teamStyle) != inputdict["Phrase"]:
                    continue
                
                # TEAM RECORDING
                resultArray["total"] += 1/validOptionsFirst/validOptionsSecond/validOptionsThird                  
                resultArray[setA.id][0] += 1/validOptionsFirst/validOptionsSecond/validOptionsThird
                resultArray[setB.id][1] += 1/validOptionsFirst/validOptionsSecond/validOptionsThird
                resultArray[setC.id][2] += 1/validOptionsFirst/validOptionsSecond/validOptionsThird
        print("Done all " + setA.id + " teams")
        foldername = "./BattleFactoryBuddy/Data/ProtoGen"
        Path(foldername).mkdir(parents=True, exist_ok=True)
        filename = foldername + "/Result.csv"
        with open (filename,"w") as o:
            o.write("Set,Position 1,Position 2, Position 3,Total\n")
            for setId in resultArray:
                if setId == "total" or resultArray["total"] == 0:
                    continue
                pos1odds = 100*resultArray[setId][0]/resultArray["total"]
                pos2odds = 100*resultArray[setId][1]/resultArray["total"]
                pos3odds = 100*resultArray[setId][2]/resultArray["total"]
                totalodds = pos1odds + pos2odds + pos3odds
                o.write(",".join([setId,str(pos1odds)+"%",str(pos2odds)+"%",str(pos3odds)+"%",str(totalodds)+"%"])+ "\n")

if __name__ == "__main__":
    inputdict = {}
    inputdict["Battle"] = "3"
    inputdict["Round"] = 8
    inputdict["Level"] = 100
    inputdict["Species1"] = "Latias"
    inputdict["Species2"] = ""
    inputdict["Species3"] = ""
    inputdict["Type"] = "None"
    inputdict["Phrase"] = "0"
    inputdict["Team1"] = ""
    inputdict["Team2"] = ""
    inputdict["Team3"] = ""
    inputdict["LastOpp1"] = ""
    inputdict["LastOpp2"] = ""
    inputdict["LastOpp3"] = ""
    t1_start = perf_counter() 
    calcAllOccurences(inputdict)
    t1_stop = perf_counter() 
    print("Elapsed time: ", t1_stop - t1_start)
    

