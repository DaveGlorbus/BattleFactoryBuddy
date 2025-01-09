import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import BattleFactoryBuddy.SwitchLogicCalculator as SwitchLogicCalculator
import BattleFactoryBuddy.StaticTeamUtils as StaticTeamUtils
setList = []
speciesList = []
for a in StaticDataHandler.StaticDataHandler.getSetList():
    setList.append(a)
    species = StaticDataHandler.StaticDataHandler.getSpeciesFromName(a.speciesName)
    if species not in speciesList:
        speciesList.append(species)
targetSpeciesDict = {}
faintedSpecies = StaticDataHandler.StaticDataHandler.getSpeciesFromName("Swampert")
#for faintedSpecies in speciesList:       
for setA in setList:
    for setB in setList:
        if setA == setB:
            continue            
        for targetSpecies in speciesList:            
            if targetSpecies == faintedSpecies:
                continue
            setAScore = setA.getSwitchScores(faintedSpecies,targetSpecies,"37")
            setBScore = setB.getSwitchScores(faintedSpecies,targetSpecies,"37")
            tempanswer = SwitchLogicCalculator.SwitchLogicCalculator.doesAcomeInOverB(setAScore, setBScore)
            setAScore = setA.getSwitchScores(faintedSpecies,targetSpecies,"40")
            setBScore = setB.getSwitchScores(faintedSpecies,targetSpecies,"40")
            if not tempanswer == SwitchLogicCalculator.SwitchLogicCalculator.doesAcomeInOverB(setAScore, setBScore):
                if targetSpecies not in targetSpeciesDict:
                    targetSpeciesDict[targetSpecies] = True
                    print("-- Magic number matters for {} over {} after {} KOs {}".format(setA.id,setB.id,targetSpecies.speciesName,faintedSpecies.speciesName))                            
"""
-- Magic number matters for Aerodactyl-3 over Alakazam-1 after Aggron KOs Aerodactyl
-- Magic number matters for Aggron-3 over Aerodactyl-3 after Quagsire KOs Aerodactyl
-- Magic number matters for Aggron-3 over Aerodactyl-3 after Swampert KOs Aerodactyl
-- Magic number matters for Aggron-3 over Aerodactyl-3 after Whiscash KOs Aerodactyl
-- Magic number matters for Ampharos-1 over Aerodactyl-4 after Cradily KOs Aerodactyl
-- Magic number matters for Blastoise-3 over Aerodactyl-4 after Gyarados KOs Aerodactyl
-- Magic number matters for Blastoise-3 over Aerodactyl-4 after Ludicolo KOs Aerodactyl
-- Magic number matters for Breloom-1 over Aerodactyl-4 after Armaldo KOs Aerodactyl
-- Magic number matters for Breloom-1 over Aerodactyl-4 after Shuckle KOs Aerodactyl
-- Magic number matters for Breloom-1 over Alakazam-2 after Forretress KOs Aerodactyl
-- Magic number matters for Breloom-1 over Alakazam-2 after Metagross KOs Aerodactyl
-- Magic number matters for Breloom-1 over Alakazam-2 after Scizor KOs Aerodactyl
-- Magic number matters for Breloom-1 over Articuno-1 after Skarmory KOs Aerodactyl
-- Magic number matters for Breloom-2 over Aerodactyl-3 after Nidoking KOs Aerodactyl
-- Magic number matters for Breloom-2 over Aerodactyl-3 after Nidoqueen KOs Aerodactyl
-- Magic number matters for Dragonite-9 over Altaria-2 after Venusaur KOs Aerodactyl
-- Magic number matters for Dragonite-9 over Altaria-2 after Victreebel KOs Aerodactyl
-- Magic number matters for Dragonite-9 over Altaria-2 after Vileplume KOs Aerodactyl
-- Magic number matters for Heracross-1 over Aerodactyl-3 after Medicham KOs Aerodactyl
-- Magic number matters for Nidoking-3 over Aerodactyl-4 after Dewgong KOs Aerodactyl
-- Magic number matters for Nidoking-3 over Aerodactyl-4 after Kingdra KOs Aerodactyl
-- Magic number matters for Nidoking-3 over Aerodactyl-4 after Lapras KOs Aerodactyl
-- Magic number matters for Nidoking-3 over Aerodactyl-4 after Walrein KOs Aerodactyl"""