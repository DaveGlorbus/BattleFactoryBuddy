import BattleFactoryBuddy.Set as Set
import BattleFactoryBuddy.Species as Species
import BattleFactoryBuddy.Move as Move
import BattleFactoryBuddy.StaticHTMLHandler as StaticHTMLHandler
import BattleFactoryBuddy.StaticMoveDataHandler as StaticMoveDataHandler
import os
import json


class StaticDataHandler:
    # Loading and initialization of all static data used by the Buddy. This is loaded once and
    # is immutable over the lifetime of the app. Only exception are the team lists which are
    # loaded on demand to improve startup performance (but are also immutable).
    version = "2.3.0"

    # Indexed by SetID (sequential numbers), contains Set objects.
    setDict = {}
    setNameDict = {}
    
    # Indexed by Species name, contains Species objects.
    speciesDict = {}

    # List of all Species Names
    speciesNameList = []
    
    # List of the names of all items
    itemList = []
    
    # Nested dictionaires indexed by Type and then Phrase, contains a list of thruples of SetIDs relating to valid
    teamLists = {}
    # Flat list of all sets (unordered)
    setList = []
    setListNames = []
    # Whether we cache teams into memory or load from file for each query.
    cacheTeams = True

    # HTML for the lists of mons / moves / items
    moveHtml = ""
    speciesHtml = ""
    itemHtml = ""    

    #H2H dict
    h2hDict = {} 

    # Pull all Set info. Add the sets to our set dict and create Species containers, adding to
    # those too.
    with open("./BattleFactoryBuddy/InputData/allpkmn.csv") as f:
        for line in f:
            set = Set.Set(line.strip().split(","))
            speciesName = set.getSpeciesName()

            # Create a new species if we don't have one.
            if speciesName not in speciesDict:
                species = Species.Species(speciesName)
                speciesDict[speciesName] = species
                speciesNameList.append(speciesName)

            # Add this set to the Species, does some further initialisation if this is the first time.
            speciesDict[speciesName].addSet(set)
            setDict[set.uid] = set
            setNameDict[set.id] = set
            setList.append(set)
            setListNames.append(set.id)
            for move in set.moveList:
                StaticMoveDataHandler.StaticMoveDataHandler.addUsedMove(move)                
            
            # Save off the item so we can populate static HTML with a full item list.
            if set.item not in itemList:
                itemList.append(set.item)
    
    # Initialise all the static HTML (mons, items, moves) that we need to inject into the web page.    
    speciesNameList.sort()
    speciesHtml = StaticHTMLHandler.StaticHTMLHandler.createListHTMLfromList(speciesNameList)
    itemList.sort()
    itemHtml = StaticHTMLHandler.StaticHTMLHandler.createListHTMLfromList(itemList)
    setHtml = StaticHTMLHandler.StaticHTMLHandler.createListHTMLfromList(setListNames)

    # Returns an unordered list of all Sets.
    @staticmethod
    def getSetList():
        return StaticDataHandler.setList

    # Returns a set matching a given ID.
    @staticmethod
    def getSetFromId(id):
        return StaticDataHandler.setDict[id]

    # Returns a set matching a given ID.
    @staticmethod
    def getSetFromName(name):
        if "10" in name:
            name = name.replace("10","X")
        return StaticDataHandler.setNameDict[name]
    
    # Returns a human readable ID (e.g. Blaziken-1) from a uid (e.g. 67)
    # Note that the method name is slightly ambiguous but is in keeping
    # with other uses across the app.
    @staticmethod
    def getNameFromId(id):
        return StaticDataHandler.setDict[id].id

    # Returns the Species matching a given ID.
    @staticmethod
    def getSpeciesFromId(id):        
        set = StaticDataHandler.setDict[id]
        speciesName = set.getSpeciesName()
        species = StaticDataHandler.speciesDict[speciesName]
        return species

    # Return the Species name matching a given ID
    @staticmethod
    def getSpeciesNameFromId(id):        
        set = StaticDataHandler.setDict[id]
        speciesName = set.getSpeciesName()
        return speciesName

    @staticmethod
    def getSpeciesFromName(speciesName):
        return StaticDataHandler.speciesDict[speciesName]
    
    @staticmethod
    def getIDsFromSpeciesName(speciesName):
        return(StaticDataHandler.getSpeciesFromName(speciesName).getIDs())

    # A utility method for other utility methods. Load all teams into cache.
    @staticmethod
    def populateCache():
        filenames = os.listdir("./BattleFactoryBuddy/Data")        
        for filename in filenames:
            if ".csv" in filename and "-" in filename:
                type = filename.split("-")[0]
                phrase = filename.split("-")[1].split(".")[0]
                for team in StaticDataHandler.iterGetTeamList(type,phrase):
                    pass

    # An iterable method to get back one valid team given the input type and phrase.
    @staticmethod
    def iterGetTeamList(type, phrase):
        # If we're caching team lists and have already read this list then pull
        # it out of our dictionaries and yield one team at a time and drop out.        
        # Now, read it in and yield one at a time, caching if setup.
        with open("./BattleFactoryBuddy/Data/" + type + "-" + phrase + ".csv") as r:            
            for line in r:
                team = line.strip().split(",")
                yield (team)                
    
    # An iterable returning a h2h result each time for the set chosen
    @staticmethod
    def iterGetH2HResult(id,monIVs,oppIVs):
        if id.split("-")[1] == "X":
            id = id.split("-")[0] + "-10"
        if id not in StaticDataHandler.h2hDict:
            with open("./BattleFactoryBuddy/Data/"+id) as input:
                for line in input:
                    StaticDataHandler.h2hDict[id] = json.loads(line)            
        for (oppSetId, result) in StaticDataHandler.h2hDict[id].items():
            yield (oppSetId, result[monIVs + "s" + oppIVs + "s"])
    
    @staticmethod
    def getMoveHTML():        
        return(StaticMoveDataHandler.StaticMoveDataHandler.getMoveHtml())        

    @staticmethod
    def getItemHTML():
        return(StaticDataHandler.itemHtml)       

    @staticmethod
    def getSpeciesHTML():
        return(StaticDataHandler.speciesHtml)   
    
    @staticmethod
    def getVersion():
        return(StaticDataHandler.version)
    
    @staticmethod
    def getSetHTML():
        return(StaticDataHandler.setHtml)
        

                
        
