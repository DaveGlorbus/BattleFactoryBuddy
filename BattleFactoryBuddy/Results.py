import BattleFactoryBuddy.SpeciesResult as SpeciesResult
import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler


class Results:
    def __init__(self, inputdict):
        self.confirmedOpponentSetsDict = {}
        self.confirmedOpponentSpeciesNameList = []
        self.freeAgentSetsDict = {}
        self.inputdict = inputdict
        self.detailMode = "DetailMode" in inputdict
        self.probabilitySort = ("NoOdds" in inputdict) or (
            "ProbabilitySort" in inputdict
        )
        self.noOdds = "NoOdds" in inputdict
        self.validTeamAdded = False
        self.notes = []
        self.errorNotes = []
        self.teamsAdded = 0
        self.hiRes = "HiRes" in inputdict and inputdict["Species1"] != ""

        # Set up for the Mons on the opposing team and defined by the user. We always want the detailed mode on this, they must be on each team and we're interested
        # in maintaining order so the user doesn't see their third mon on top.
        idx = 1
        while idx <= 3:
            if self.inputdict["Species" + str(idx)] != "":
                self.confirmedOpponentSetsDict[self.inputdict["Species" + str(idx)]] = (
                    SpeciesResult.SpeciesResult(
                        self.inputdict["Species" + str(idx)], self.inputdict, True
                    )
                )
                self.confirmedOpponentSpeciesNameList.append(
                    self.inputdict["Species" + str(idx)]
                )
            idx += 1

    # Save a legitimate team off in this results object. It's useful to easily know whether there are any legit results so save that off separately.
    def addTeam(self, teamList, count=1):
        self.teamsAdded += 1
        for set in teamList:
            speciesName = StaticDataHandler.StaticDataHandler.getSpeciesFromId(
                set
            ).speciesName
            if speciesName in self.confirmedOpponentSetsDict:
                self.confirmedOpponentSetsDict[speciesName].addCount(set)
            else:
                if speciesName not in self.freeAgentSetsDict:
                    self.freeAgentSetsDict[speciesName] = SpeciesResult.SpeciesResult(
                        speciesName, self.inputdict
                    )
                self.freeAgentSetsDict[speciesName].addCount(set)
        if count > 1:
            newcount = count - 1
            self.addTeam(teamList, count=newcount)

    # Check whether we found any valid teams.
    def isValidTeams(self):
        return self.teamsAdded > 0

    # Iteratively return a SpeciesResult for each Species specified in the query. This can be none if our query doesn't have any defined.
    def iterGetConfirmedOpponentSpeciesResults(self):
        for confirmedOpponentSpeciesName in self.confirmedOpponentSpeciesNameList:
            yield self.confirmedOpponentSetsDict[confirmedOpponentSpeciesName]

    # Return a sorted list of all the non-specified species. The sorting here is interesting as we have several different sorting schemes based on config.
    def iterGetSortedFreeAgentSpeciesResults(self):
        # Build the list of all our name, result pairs.
        freeAgentList = []
        for speciesName, speciesResult in self.freeAgentSetsDict.items():
            freeAgentList.append((speciesName, speciesResult))
        # Sort
        if self.noOdds:
            freeAgentList.sort(key=lambda tuple: tuple[0])
        else:
            freeAgentList.sort(key=lambda tuple: tuple[1].getSortKey(), reverse=True)

        # Yield one SpeciesResult on the list at a time
        for speciesName, speciesResult in freeAgentList:
            if self.hiRes:
                speciesPercentage = speciesResult.speciesPercentage
            else:
                speciesPercentage = float(speciesResult.totalcount * 100 / self.teamsAdded)
            yield (speciesResult, speciesPercentage)
        return

    # Add an error message to be rendered back to the user.
    def addError(self, errorString):
        self.errorNotes.append(errorString)

    # Add a note to be rendered back the user.
    def addNote(self, noteString):
        self.notes.append(noteString)
    
    # Load in a list of results for Hi-def mode. The data here looks very different due to how
    # it's generated but we want a consistent interface into the HTML builder, so here's where
    # we handle the mess.
    def loadHiResResults(self, resultList):
        thisSpeciesName = ""
        currentSpeciesName = ""
        currentSpeciesList = []                
        for setAndResult in resultList:
            thisSpeciesName = setAndResult[0].speciesName
            # First time through the loop
            if currentSpeciesName == "":
                currentSpeciesName = thisSpeciesName
            if (thisSpeciesName != currentSpeciesName):                
                if currentSpeciesName in self.confirmedOpponentSetsDict:
                    self.confirmedOpponentSetsDict[currentSpeciesName].loadHiResResults(currentSpeciesList)                    
                else:
                    self.freeAgentSetsDict[currentSpeciesName] = SpeciesResult.SpeciesResult(currentSpeciesName, self.inputdict)
                    self.freeAgentSetsDict[currentSpeciesName].loadHiResResults(currentSpeciesList)                    
                currentSpeciesList = []
                self.teamsAdded += 1                
                currentSpeciesName = thisSpeciesName
            currentSpeciesList.append(setAndResult)
        
        # Pick up the final set too
        if currentSpeciesName in self.confirmedOpponentSetsDict:
            self.confirmedOpponentSetsDict[currentSpeciesName].loadHiResResults(currentSpeciesList)            
        else:
            self.freeAgentSetsDict[currentSpeciesName] = SpeciesResult.SpeciesResult(currentSpeciesName, self.inputdict)
            self.freeAgentSetsDict[currentSpeciesName].loadHiResResults(currentSpeciesList)        

