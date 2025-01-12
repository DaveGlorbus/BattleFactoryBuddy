import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import BattleFactoryBuddy.SwitchLogicCalculator as SwitchLogicCalculator
import BattleFactoryBuddy.StaticTeamUtils as StaticTeamUtils
from pathlib import Path

class SetCalcHandler:
    def __init__(self):
        return

    def calculate(self, inputdict, results):
        if "HiRes" in inputdict and inputdict["Species1"] != None:
            return self.calcProcedural(inputdict,results)
        elif inputdict["Battle"] == "15":
            return self.calculateNolandBattle(inputdict, results)
        else:
            return self.calculateStandardBattle(inputdict, results)

    def generateListOfDictsOfRequiredSets(self, inputdict,overrideSetTo3 = False):
        requiredListList = []
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
                requiredDict = {}
                for id in StaticDataHandler.StaticDataHandler.getSpeciesFromName(
                        inputdict["Species" + str(idx)]
                    ).filter(moves, items, ids if not overrideSetTo3 else ['3']):
                    requiredDict[id] = 1
                requiredListList.append(requiredDict)
            idx += 1
        return requiredListList

    def calculateStandardBattle(self, inputdict, results):
        # Get list of lists of required sets to be present in teams that are possible.
        # These are set IDs.
        requiredDictsList = self.generateListOfDictsOfRequiredSets(inputdict)

        # Create a dict of setIDs that aren't allowed. This is all the sets of
        # all species that are on the team or the last team (or draft)
        unallowedDict = {}
        for speciesName in (inputdict["Team1"],inputdict["Team2"],inputdict["Team3"],inputdict["LastOpp1"],inputdict["LastOpp2"],inputdict["LastOpp3"]):
            if speciesName == "":
                continue
            for setID in StaticDataHandler.StaticDataHandler.getIDsFromSpeciesName(speciesName):
                unallowedDict[setID] = 1

        # Create the list of team sets that are allowed, based on round and level.
        teamSetList = []
        level = inputdict["Level"]
        round = inputdict["Round"]

        # ALTSETS - if you have different rules on which teams are in which rounds then change it here.
        if (level == "50" and round == "8") or (level == "100" and int(round) > 4):
            teamSetList += ["5"]
            if level == "100":
                teamSetList += ["6"]
            teamSetList += ["4", "3", "2", "1"]
        elif (level == "50" and round == "7") or (level == "100" and round == "4"):
            teamSetList += ["4"]
        elif (level == "50" and round == "6") or (level == "100" and round == "3"):
            teamSetList += ["3"]
        elif (level == "50" and round == "5") or (level == "100" and round == "2"):
            teamSetList += ["2"]
        elif (level == "50" and round == "4") or (level == "100" and round == "1"):
            teamSetList += ["1"]

        # Calculate any required info up front about which calcs we need to do, so
        # we've got a simple bool to check in the big loop.
        switchlogic = False
        if (
           "targetmon" in inputdict
            and inputdict["targetmon"] != ""
            and inputdict["Species2"] != ""
            and inputdict["Species1"] != ""
        ):
            switchlogic = True
            if(inputdict["magicnumber"] == ""):
                magicNumber = "40"
            else:
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

        # Take a deep breath and pull each possible team one at a time from the
        # StaticDataHandler's iterable method.
        for teamData in StaticDataHandler.StaticDataHandler.iterGetTeamList(
            inputdict["Type"], inputdict["Phrase"]
        ):
            # Check whether the round indicator on the team is matches the round we're in.
            team = teamData[0:3]
            roundData = teamData[3]
            if roundData not in teamSetList:
                continue

            # Check we've got one of each of the required mons
            if len(requiredDictsList) > 0:
                foundrequired = False
                for requiredDict in requiredDictsList:
                    foundrequired = False
                    for set in team:
                        if set in requiredDict:
                            foundrequired = True
                            break                    
                    if not foundrequired:
                        break
                # We can only leave the previous loop "happily" if we ended by find a suitable set match. Otherwise loop onto
                # the next team
                if not foundrequired:
                    continue

            # Check we don't have any of the mons we shouldn't have.
            foundDisallowed = False
            for set in team:                
                if set in unallowedDict:
                    foundDisallowed = True
                    break
            if foundDisallowed:
                continue

            # Run switch logic. We assume that A B C is as likely as A C B and therefore if B always
            # comes in over C it's twice as likely that this team is what's happened. If C always
            # comes in over B, but we've got B in front of us then it's an impossible team.
            # Note, we can only do anything here if we've already had 2 mons defined for us, which
            # cuts down the number of sets we can be dealing with a lot. We therefore chose to
            # recalc some stuff here to keep the above code neat and tidy.
            if switchlogic:
                # Get the switch scores for Species2 and Species3 (which may or may not have been defined).
                for set in team:
                    speciesName = StaticDataHandler.StaticDataHandler.getSpeciesFromId(
                        set
                    ).speciesName
                    if speciesName == inputdict["Species2"]:
                        species2SwitchScores = (
                            StaticDataHandler.StaticDataHandler.getSetFromId(
                                set
                            ).getSwitchScores(
                                faintedSpecies, targetSpecies, magicNumber
                            )
                        )
                    elif speciesName != inputdict["Species1"]:
                        species3SwitchScores = (
                            StaticDataHandler.StaticDataHandler.getSetFromId(
                                set
                            ).getSwitchScores(
                                faintedSpecies, targetSpecies, magicNumber
                            )
                        )

                if inputdict["Species3"] != "" and inputdict["ballnum"] != "":
                    addCount = SwitchLogicCalculator.SwitchLogicCalculator.getTeamCountFromSwitchScoresValWithBall(
                        species2SwitchScores, species3SwitchScores, inputdict["ballnum"]
                    )
                else:
                    addCount = SwitchLogicCalculator.SwitchLogicCalculator.getTeamCountFromSwitchScoresVal(
                        species2SwitchScores, species3SwitchScores
                    )
                if addCount > 0:
                    results.addTeam(team, addCount)

            # We've got a valid team and how many we want it to count for. Save that off in our results object.
            else:
                results.addTeam(team)
        return results

    # What to work out and display for Noland battles is quite tricky. We don't want to have to trawl
    # through too much stuff but there is value we can add by eliminating through item clause and doing
    # switch logic if its applicable.
    # NOTE: We don't get here if we don't have at least one species defined, that's handled in validation.
    def calculateNolandBattle(self, inputdict, results):
        switchin = False
        if (
            "targetmon" in inputdict
            and inputdict["targetmon"] != ""
            and inputdict["Species2"] != ""
            and inputdict["Species1"] != ""
        ):
            switchin = True
            if(inputdict["magicnumber"] == ""):
                magicNumber = "40"
            else:
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

        # If this is round 6 L50 or round 3 OL then Noland is limited to set 3 mons. Work that out so
        # we can filter to only the ones that are possible.
        overrideSetTo3 = False
        if inputdict["Level"] == "50" and inputdict["Round"] == "6":
            overrideSetTo3 = True
        elif inputdict["Level"] == "100" and inputdict["Round"] == "3":
            overrideSetTo3 = True

        # Get all the possible sets we've seen from Noland.
        requiredListList = self.generateListOfDictsOfRequiredSets(inputdict, overrideSetTo3=overrideSetTo3)

        # If we've not got anything species specified then the query handler will have returned an error.

        # If we've only got one species defined then just add them all equally so people can filter them.
        if inputdict["Species1"] != "" and inputdict["Species2"] == "":
            resultNote = "Noland battle - not attempting to calculate mons in the back"
            results.addNote(resultNote)
            for requiredList in requiredListList:
                for set in requiredList:
                    results.addTeam([set, set, set])
        # If we've got two or three species then we can some switch-in and item logic.
        else:
            species1Ids = requiredListList[0]
            species2Ids = requiredListList[1]
            if (
                inputdict["Species1"] != ""
                and inputdict["Species2"] != ""
                and inputdict["Species3"] == ""
            ):
                species3Sets = StaticDataHandler.StaticDataHandler.getSetList()
            else:
                # We need to get all these sets to make the loop below work.
                species3Sets = []
                species3Ids = requiredListList[2]
                for id in species3Ids:
                    species3Sets.append(
                        StaticDataHandler.StaticDataHandler.getSetFromId(id)
                    )
            for s1Id in species1Ids:
                s1set = StaticDataHandler.StaticDataHandler.getSetFromId(s1Id)
                for s2Id in species2Ids:
                    s2set = StaticDataHandler.StaticDataHandler.getSetFromId(s2Id)
                    if s1set.compatibilitycheck(s2set):
                        # We don't have an easy way to get all IDs so this one just goes straight from sets.
                        for s3set in species3Sets:
                            if s1set.compatibilitycheck(
                                s3set
                            ) and s2set.compatibilitycheck(s3set):
                                if switchin:
                                    species2SwitchScores = s2set.getSwitchScores(
                                        faintedSpecies, targetSpecies, magicNumber
                                    )
                                    species3SwitchScores = s3set.getSwitchScores(
                                        faintedSpecies, targetSpecies, magicNumber
                                    )
                                    if (
                                        inputdict["Species3"] != ""
                                        and inputdict["ballnum"] != ""
                                    ):
                                        addCount = SwitchLogicCalculator.SwitchLogicCalculator.getTeamCountFromSwitchScoresValWithBall(
                                            species2SwitchScores,
                                            species3SwitchScores,
                                            inputdict["ballnum"],
                                        )
                                    else:
                                        addCount = SwitchLogicCalculator.SwitchLogicCalculator.getTeamCountFromSwitchScoresVal(
                                            species2SwitchScores, species3SwitchScores
                                        )
                                    if addCount > 0:
                                        results.addTeam(
                                            (s1Id, s2Id, s3set.uid), addCount
                                        )
                                else:
                                    results.addTeam((s1Id, s2Id, s3set.uid))
        return results
    
    def calcProcedural(self,inputdict,results):        
        validOptionsFirst = len(StaticDataHandler.StaticDataHandler.getSetList())    
        # CREATE RESULTS ARRAY
        resultArray = {}    
        resultArray["total"] = 0
        noland = inputdict["Battle"] == "15"

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
            "targetmon" in inputdict
            and inputdict["targetmon"] != ""
            and inputdict["Species2"] != ""
            and inputdict["Species1"] != ""
        ):
            switchlogic = True
            if(inputdict["magicnumber"] == ""):
                magicNumber = "40"
            else:
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
                    # Precalc switchins
            switchScoreDict = {}        
            for set in setList:
                switchScoreDict[set.id] = {}
                switchScoreDict[set.id][magicNumber] = set.getSwitchScores(faintedSpecies,targetSpecies,magicNumber)


            

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
                    if not noland:
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

                        setBScore = switchScoreDict[setB.id][magicNumber]
                        setCScore = switchScoreDict[setB.id][magicNumber]                        
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
        resultList = []        
        for setId in resultArray:
            if setId == "total" or resultArray["total"] == 0 or resultArray[setId] == 0:
                    continue
            totalodds = 100*resultArray[setId]/resultArray["total"]                
            resultList.append([StaticDataHandler.StaticDataHandler.getSetFromName(setId),totalodds])                    
        results.loadHiResResults(resultList)        
        return(results)
