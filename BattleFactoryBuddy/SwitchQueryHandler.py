import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import BattleFactoryBuddy.SwitchLogicCalculator as SwitchLogicCalculator
import BattleFactoryBuddy.SwitchQueryHTMLHandler as SwitchQueryHTMLHandler

class SwitchQueryHandler:
    def __init__(self, inputdict):
        self.inputdict = inputdict
        
    
    def handleQuery(self):
        htmlHandler = SwitchQueryHTMLHandler.SwitchQueryHTMLHandler()
        species1Name = self.inputdict["candidatemon1"]
        species2Name = self.inputdict["candidatemon2"]
        faintedSpecies = StaticDataHandler.StaticDataHandler.getSpeciesFromName(self.inputdict["faintedmon"])
        targetSpecies = StaticDataHandler.StaticDataHandler.getSpeciesFromName(self.inputdict["targetmon"])
        
        results = SwitchResults(species1Name, species2Name)        
        # Get the results for each set from species 1
        for species1setId in StaticDataHandler.StaticDataHandler.getSpeciesFromName(species1Name).filter():
            species1set = StaticDataHandler.StaticDataHandler.getSetFromId(species1setId)
            species1result = species1set.getSwitchScores(faintedSpecies,targetSpecies,magicNumber)
            results.addSetResult(species1Name,species1setId,species1result)

            # Get the results for each set from species 2
            if species2Name != "" and species2Name != "cm2":
                for species2setId in StaticDataHandler.StaticDataHandler.getSpeciesFromName(species2Name).filter():
                    species2set = StaticDataHandler.StaticDataHandler.getSetFromId(species2setId)
                    species2result = species2set.getSwitchScores(faintedSpecies,targetSpecies,magicNumber)
                    results.addSetResult(species2Name,species2setId,species2result)

                    # Work out the H2H and save that off.
                    h2hvalue = SwitchLogicCalculator.SwitchLogicCalculator.doesAcomeInOverB(species1result, species2result) - SwitchLogicCalculator.SwitchLogicCalculator.doesAcomeInOverB(species2result, species1result)
                    if h2hvalue == 1:
                        resultString = str(species1set.id)
                    elif h2hvalue == -1:
                        resultString = str(species2set.id)
                    else:
                        resultString = "<font color=\"#808080\">Either"
                    results.addH2Hresult(species1setId,species2setId, resultString)
        self.inputdict = htmlHandler.generateHTML(self.inputdict,results)        
        return(self.inputdict)

class SwitchResults:
    def __init__(self, species1, species2):
        self.switchResultsDict = {}
        self.switchResultsDict[species1] = {}
        if species2 != "" and species2 != "cm2":
            self.switchResultsDict[species2] = {}        
        self.h2hResultsDict = {}
    
    def addSetResult(self,speciesName,setId,setResult):        
        self.switchResultsDict[speciesName][setId] = setResult
    
    def addH2Hresult(self, species1setId,species2setId, resultString):
        if species1setId not in self.h2hResultsDict:
            self.h2hResultsDict[species1setId] = {}
        self.h2hResultsDict[species1setId][species2setId] = resultString
    
    def iterGetSetResult(self,speciesName):
        for setId, result in self.switchResultsDict[speciesName].getItems():
            yield(setId, result)
    
    

                        
        
        