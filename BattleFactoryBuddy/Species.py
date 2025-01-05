# A class representing a collection of all the Sets in a Species.
class Species:
    def __init__(self, speciesName):
        self.speciesName = speciesName
        self.setList = [] 
        self.fullyInit = False       
        self.types = []
        self.IDs = []
    
    # Add a set to this species during initialisation.
    def addSet(self, set):    
        if not self.fullyInit:
            self.types = set.getTypes()
            self.abilities = set.getAbilities()
            self.fullyInit = True    
        self.setList.append(set)
        self.IDs.append(set.uid)
    
    # Return a list of Set.uids matching those filtered. Up to the calling code to handle
    # the case where there aren't any.
    # NOTE REMOVED AN ITEMOUT FIELD FROM THIS DEFINITION.
    def filter(self, movesin=[], itemin=[], ids=[],returnSets = False):
        retlist = []        
        for set in self.setList:
            satisfied = True         
            # If any IDs have been manually entered, check we match one.
            if ids != []:                                
                localvalid = False
                for id in ids:                       
                    if str(id) in set.id:
                        localvalid = True
                if not localvalid:                            
                    satisfied = False
            # If any moves have been specified, check this set has it.
            for move in movesin:                
                if move not in set.moveList:                    
                    satisfied = False
            # If an item has been specified, check this set has it.
            for item in itemin:
                if item != set.item:                     
                    satisfied = False
            if satisfied:
                if returnSets:
                    retlist.append(set)                
                else:
                    retlist.append(set.uid)
        
        if len(retlist) == 0:
            print("Returned no sets for " + self.speciesName + ", likely error on input")        
        return(retlist)
    
    # Just get the list of IDs.
    def getIDs(self):
        return(self.IDs)


