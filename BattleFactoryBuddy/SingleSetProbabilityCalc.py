import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import BattleFactoryBuddy.Team as Team
import BattleFactoryBuddy.StaticTeamUtils as StaticTeamUtils
import BattleFactoryBuddy.SwitchLogicCalculator as SwitchLogicCalculator
import random
from time import perf_counter
from pathlib import Path

# RUN THIS USING calcSetOdds.bat
# Alter the fixed mons by changing the lockspecies
# Create a directory called 

def calcAllOccurences(inputdict,results,write=False):    
    t1_start = perf_counter() 
    validOptionsFirst = len(StaticDataHandler.StaticDataHandler.getSetList())    
    # CREATE RESULTS ARRAY
    resultArray = {}    
    resultArray["total"] = 0

    # Allowed round markers
    checkround = False
    if inputdict["Level"] != "100" or inputdict["Round"] not in ["5","6","7","8"]:
        checkround = True
        markers = []
        if inputdict["Level"] == "50" and inputdict["Round"] == "8":
            markers = ["1","2","3","4","5"]
        else:
            markerval = int(inputdict["Round"])
            if inputdict["Level"] == "50":
                markerval = markerval-3           
            if markerval < 1:
                print("Bad round input")
                return
            else:
                markers=[str(markerval)]        

    # SET UP LIST OF MONS VALID FOR THESE TEAMS
    blockedSpecies = [inputdict["Team1"],inputdict["Team2"],inputdict["Team3"],inputdict["LastOpp1"],inputdict["LastOpp2"],inputdict["LastOpp3"],inputdict["Species1"],inputdict["Species2"],inputdict["Species3"]]
    while "" in blockedSpecies:
        blockedSpecies.remove("")
    setList = []
    firstSetList = []

    # Populate list with filtered sets for any Species defined.
    idx = 1
    while idx <= 3:
        if inputdict["Species" + str(idx)] != "":
            moves = [
                inputdict["Move1" + str(idx)],
                inputdict["Move2" + str(idx)],
                inputdict["Move3" + str(idx)],
                inputdict["Move4" + str(idx)],
            ]
            while "" in moves:
                moves.remove("")
            items = [inputdict["Item" + str(idx)]]
            while "" in items:
                items.remove("")
            ids = inputdict["Set" + str(idx)].split(",")
            while "" in ids:
                ids.remove("")            
            for set in StaticDataHandler.StaticDataHandler.getSpeciesFromName(
                    inputdict["Species" + str(idx)]
                ).filter(moves, items, ids, True):
                if not checkround or set.roundInfo in markers:
                    resultArray[set.id] = 0        
                    if idx == 1:
                        firstSetList.append(set)
                    else:
                        setList.append(set)            
        idx += 1

    # Prep the setList for any mon not defined
    for set in StaticDataHandler.StaticDataHandler.getSetList():        
        if (checkround):            
            if set.roundInfo not in markers:                
                continue                
        if set.speciesName in blockedSpecies:
            continue
        resultArray[set.id] = 0        
        setList.append(set)
    if firstSetList == []:
        firstSetList = setList
    validOptionsFirst = len(firstSetList)    

    # Prep switch logic
    switchlogic = False
    if (
        "switchin" in inputdict
        and "targetmon" in inputdict
        and inputdict["targetmon"] != ""
        and inputdict["Species2"] != ""
        and inputdict["Species1"] != ""
    ):
        switchlogic = True
        if "magicnumber" not in inputdict or inputdict["magicnumber"] == "":
            inputdict["magicnumber"] = 40
        magicNumber = inputdict["magicnumber"]
        faintedSpecies = StaticDataHandler.StaticDataHandler.getSpeciesFromName(
            inputdict["Species1"]
        )
        targetSpecies = StaticDataHandler.StaticDataHandler.getSpeciesFromName(
            inputdict["targetmon"]
        )
        resultNote = "Calculating assuming {} switched in when {} KO'd {}".format(
            inputdict["Species2"], inputdict["targetmon"], inputdict["Species1"]
        )
        if inputdict["ballnum"] != "" and inputdict["Species3"] != "":
            resultNote += ", and that {} was in ball {}".format(
                inputdict["Species2"], inputdict["ballnum"]
            )
        results.addNote(resultNote)

    # DO THE THING
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

                # Do switch logic. Note that it's way easier here. We'll get to the other order
                # later so just think about what's in front of us.
                if switchlogic:
                    if inputdict["ballnum"] == "2":
                        if setB.speciesName != inputdict["Species2"]:
                            continue
                    elif inputdict["ballnum"] == "3":
                        if setB.speciesName != inputdict["Species3"]:
                            continue

                    setBScore = setB.getSwitchScores(faintedSpecies,targetSpecies,magicNumber)
                    setCScore = setC.getSwitchScores(faintedSpecies,targetSpecies,magicNumber)
                    if setB.speciesName == inputdict["Species2"]:                        
                        if not SwitchLogicCalculator.SwitchLogicCalculator.doesAcomeInOverB(setBScore, setCScore):                            
                            continue
                    elif setC.speciesName == inputdict["Species2"]:
                        if SwitchLogicCalculator.SwitchLogicCalculator.doesAcomeInOverB(setBScore, setCScore):                            
                            continue
                    else:
                        print("WHERE IS SPECIES 2?")

                # TEAM RECORDING
                resultArray["total"] += 1/validOptionsFirst/validOptionsSecond/validOptionsThird                  
                resultArray[setA.id] += 1/validOptionsFirst/validOptionsSecond/validOptionsThird
                resultArray[setB.id] += 1/validOptionsFirst/validOptionsSecond/validOptionsThird
                resultArray[setC.id] += 1/validOptionsFirst/validOptionsSecond/validOptionsThird
        print("Done all " + setA.id + " teams")
    if (write):
        foldername = "./BattleFactoryBuddy/Data/ProtoGen"
        Path(foldername).mkdir(parents=True, exist_ok=True)
        filename = foldername + "/Result.csv"
        with open (filename,"w") as o:
            o.write("Set,Total\n")
            for setId in resultArray:
                if setId == "total" or resultArray["total"] == 0:
                    continue
                totalodds = 100*resultArray[setId]/resultArray["total"]                
                o.write(",  ".join([setId,"{:.2f}%".format(totalodds)])+ "\n")
    else:        
        resultList = []        
        for setId in resultArray:
            if setId == "total" or resultArray["total"] == 0 or resultArray[setId] == 0:
                    continue
            totalodds = 100*resultArray[setId]/resultArray["total"]                
            resultList.append([StaticDataHandler.StaticDataHandler.getSetFromName(setId),totalodds])                    
        results.loadHiResResults(resultList)        
        return(results)

if __name__ == "__main__":
    inputdict = {}
    inputdict["Battle"] = "3"
    inputdict["Round"] = "8"
    inputdict["Level"] = "100"
    inputdict["Species1"] = "Walrein"
    inputdict["Species2"] = "Lapras"
    inputdict["Species3"] = ""
    inputdict["Type"] = "None"
    inputdict["Phrase"] = "0"
    inputdict["Team1"] = ""
    inputdict["Team2"] = ""
    inputdict["Team3"] = ""
    inputdict["LastOpp1"] = ""
    inputdict["LastOpp2"] = ""
    inputdict["LastOpp3"] = ""
    inputdict["Move11"] = ""
    inputdict["Move21"] = ""
    inputdict["Move31"] = ""
    inputdict["Move41"] = ""
    inputdict["Move12"] = ""
    inputdict["Move22"] = ""
    inputdict["Move32"] = ""
    inputdict["Move42"] = ""
    inputdict["Move13"] = ""
    inputdict["Move23"] = ""
    inputdict["Move33"] = ""
    inputdict["Move43"] = ""
    inputdict["Item1"] = ""
    inputdict["Item2"] = ""
    inputdict["Item3"] = ""
    inputdict["Set1"] = ""
    inputdict["Set2"] = "4,6,7,8"
    inputdict["Set3"] = ""
    t1_start = perf_counter() 
    calcAllOccurences(inputdict,"",True)
    t1_stop = perf_counter() 
    print("Elapsed time: ", t1_stop - t1_start)
    

