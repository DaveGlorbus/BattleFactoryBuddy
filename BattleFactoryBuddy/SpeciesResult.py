import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler

class SpeciesResult():
    def __init__(self, speciesName, inputdict, confirmedOpponent=False):
        self.totalcount = 0
        self.speciesName = speciesName
        self.setDict = {}
        self.hiResResultList = []
        # This field covers whether we're tracking the distribution of different sets or just the chance
        # of the species being shown. This is True for mons that have been seen on the opponent's team and
        # for everything if the "Sets on upcoming mons" is set.
        self.setCollation = confirmedOpponent or ("DetailMode" in inputdict) or ("NoOdds" in inputdict)
        self.sortOnProbability = not ("NoOdds" in inputdict) and ("ProbabilitySort" in inputdict)
        self.noOdds = ("NoOdds" in inputdict)
        self.speciesPercentage = 0
    
    def addCount(self, setid=None):
        self.totalcount += 1
        if ((setid != None) and (self.setCollation)):
            if setid not in self.setDict:
                self.setDict[setid] = 0
            self.setDict[setid] += 1
    
   
    # Provide a key for sorting based on results. This needs to be number of instances with alphabetical order
    # as a tiebreak. We don't know what we're going to be compared against so have to be careful here that 
    # we're using suitable padding and making everything work. 
    # The scheme we go for is YXXX where Y is the totalcount and XXX is 1000- number of an arbitrary set.
    # This would sort [(Aero, 5 instances),(Starmie, 5 instances),(Zapdos, 6 instances)] correctly
    # as Zapdos, Aero, Starmie
    # It'd be nice to override __gt__ or __lt__ here but sometimes we want to sort on other things.
    # I'd accept pull requests to make this less hokey.
    def getSortKey(self):
        if self.hiResResultList == []:
            return self.totalcount*1000 + (1000 - int(StaticDataHandler.StaticDataHandler.getSpeciesFromName(self.speciesName).setList[0].getuid()))
        else:
            return self.speciesPercentage*10000000 + (1000 - int(StaticDataHandler.StaticDataHandler.getSpeciesFromName(self.speciesName).setList[0].getuid()))

    # Return the sets under this SpeciesResult. This should only be called if setCollation is true (otherwise, why would we care?) and
    # sorts the sets under it based on configuration (e.g. no odds mode etc.)
    def iterGetSets(self):
        if not self.setCollation:
            raise "Trying to pull out a set when we're not configured to."
        
        if self.hiResResultList != []:
            for setAndResult in self.hiResResultList:
                tuple = (setAndResult[1],setAndResult[0])
                #print(setAndResult[1],setAndResult[0].id)
                yield(tuple)

        else:    
            # Get our sets into a list.
            setList = []
            for (setId, setResult) in self.setDict.items():
                setList.append((setId,setResult)) 
            
            # Sort alphabetically first, then sort by incidences. This is max 10 entries so the perf hit of sorting twice is fine and saves
            # us having to create an object for a key method as above or creating an awful lambda expression.
            setList.sort(key=lambda tuple: tuple[0])
            if self.sortOnProbability:            
                setList.sort(key=lambda tuple: tuple[1], reverse=True)
            for (setId,setResult) in setList:            
                if self.noOdds:
                    tuple = ("",StaticDataHandler.StaticDataHandler.getSetFromId(setId))
                else:
                    tuple = (float(setResult*100)/self.totalcount, StaticDataHandler.StaticDataHandler.getSetFromId(setId))                

                yield(tuple)
            return
    
    def loadHiResResults(self, resultList):
        self.hiResResultList = resultList
        self.hiResResultList.sort(key=lambda tuple: tuple[1], reverse=True)
        for result in self.hiResResultList:
            self.speciesPercentage += result[1]        
        #print(self.speciesName, resultList[0][0].id)    

        

            
