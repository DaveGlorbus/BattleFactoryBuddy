import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import BattleFactoryBuddy.Team as Team
import json

# Script to generate all static data (teams and speed tiers) and save them off in CSV files. This allows us to precompute all available teams
# once and not have to do it per query (which would be prohibitively slow). These files are also large so aren't checked in
# and need to be generated per-checkout or if the underlying mon data changes.

# Spin through all combinations of 3 mons. For each combination see if they're a valid team. If they are, work out which phrase they go with.
# Once we've done that then write them into csvs using their uids for brevity.
def generateTeamList():
    print("Starting generating team lists")
    setList = StaticDataHandler.StaticDataHandler.getSetList()
    maxpkmn = len(setList)
    validcombocount=0
    # Initialise looking at sets 1, 2 and 3 and work from there.
    a = 0
    b = 1
    c = 2
    combodictcount= {}
    while a < maxpkmn:
        setA = setList[a]
        while (b < maxpkmn):
            setB = setList[b]
            if (setA.compatibilitycheck(setB)):
                while (c < maxpkmn):
                    setC = setList[c]                
                    if((setA.compatibilitycheck(setC))):
                        if((setB.compatibilitycheck(setC))):                                
                            validcombocount +=1
                            team = Team.Team(setA,setB,setC)              
                            if team.round == "0":
                                setC=None
                                c+=1
                                continue
                            type = team.type                                
                            style = team.style                            
                            if type in combodictcount:
                                if style in combodictcount[type]:
                                    combodictcount[type][style].append(team.shortStr())
                                else:
                                    combodictcount[type][style] = [team.shortStr()]
                            else:
                                combodictcount[type] = {}
                                combodictcount[type][style] = [team.shortStr()]                                                    
                    setC=None
                    c+=1
            setB=None
            setC=None
            b+=1
            c=b+1
        print("Done with all " + setA.id + " teams!")
        setA = None
        setB = None
        setC = None
        # Reinitialise with the next 3 sets.
        a+=1
        b=a+1
        c=a+2

    # Write out the CSVs.
    print("Created " + str(validcombocount) + " teams! Start writing them in sets")
    for a in combodictcount:
        for b in combodictcount[a]:
            with open ("./BattleFactoryBuddy/Data/"+str(a) + "-" + str(b) + ".csv","w") as o:
                for teamStr in combodictcount[a][b]:
                    o.write(teamStr + "\n")
                print("Written to ../Data/"+str(a) + "-" + str(b) + ".csv")

# A utility function for checking the data on set moves and their phrases is consistent.
# As an example, the base spreadsheet for factory had Registeel-3 as 0 0 4 4 whereas Amnesia
# meant it should have been 0 1 4 4, this catches those issues (especially useful if you've edited the sets for some reason).
def validateSetInfo():
    setList = StaticDataHandler.StaticDataHandler.getSetList()
    movedict = {}
    typesdict = {}
    for set in setList:
        i = 0
        while i < 4:
            move = set.moveList[i]
            cat = set.moves.split(" ")[i]
            if move not in movedict:
                movedict[move] = cat
            else:
                if movedict[move] != cat:
                    print("Mistmatch on %s, found %s saved as %s. \nFix allpkmn.csv and rerun."%(move,cat,movedict[move]))
                    exit()
            i += 1
        if set.speciesName not in typesdict:            
            typesdict[set.speciesName] = sorted(set.types)
        elif typesdict[set.speciesName] != sorted(set.types):
            print("Type mismatch on %s, saved off as %s and found as %s. \nFix allpkmn.csv and rerun."%(set.speciesName,typesdict[set.speciesName],set.types))
            exit()

# Create inidividual matchup files out of the massive json checked-in.
def generateH2Hfiles():
    print("Generating H2H files for the team builder.")
    with open("./BattleFactoryBuddy/InputData/combined_data_lv_50_20_battles.json") as input:
        for line in input:
            h2hDict = json.loads(line)
            break    
    for key in h2hDict:
        with open("./BattleFactoryBuddy/Data/"+key,"w") as output:            
            writestr = ""
            newdict = {}
            for key2 in h2hDict[key]:                
                if key == key2:
                    continue
                newdict[key2] = h2hDict[key][key2]                   
            writestr = json.dumps(newdict)
            output.write(writestr)
            print("Written teambuilder info for " + key)            

# UNUSED
# ALTSETS - provide an updated battle_moves.h in this directory if you need to update the move data. This list is small enough
# and distinct enough from the source data that it's just included in the repo for standard factory usage. You'll need
# to uncomment the function call below if you want it to run.
def generateMoveList():
    try:
        with open("./BattleFactoryBuddy/InputData/battle_moves.h") as r:
            with open(".BattleFactoryBuddy/InputData/moves.csv","w") as w:
                currmove = []
                for line in r:
                    if "[MOVE_" in line:                
                        if currmove != []:
                            w.write(",".join(currmove) + "\n")                
                        currmove = [line.split("MOVE_")[1].split("]")[0]]
                    elif "=" in line and currmove != []:    
                        if ".type" in line:
                            currmove.append(line.split("TYPE_")[1].split(",")[0])

                        else:
                            currmove.append(line.split("=")[1].split(",")[0])
                    else:
                        continue
                w.write(",".join(currmove) + "\n")
    except:
        print("Using standard move data - not generating.")

# UNUSED
# A silly little utility function to count the instances of each move, not run by default.
def generateMoveCounts():
    movedict = {}
    setList = StaticDataHandler.StaticDataHandler.getSetList()
    for set in setList:
        for move in set.moveList:
            if move not in movedict:
                movedict[move] = 1
            else:
                movedict[move] += 1
    with open("./BattleFactoryBuddy/Data/movecounts.csv","w") as o:
        for move in movedict:
            outstr = move + "," + str(movedict[move]) + "\n"
            o.write(outstr)

# UNUSED
# ALTSETS - if you've changed the type chart then you can use this autogenerate a bunch of code used to work out type effectiveness.
def generateTypeEffectivenessCode():
    with open("./types.csv") as r:
        currenttype = None
        prefill = "\tif \"{}\" in targettypes:\n\t\tretval = int(retval*{})"
        for line in r:
            split = line.strip().split(" ")        
            if split[0] != currenttype:
                print("elif intype == \"{}\":".format(split[0]))
                currenttype = split[0]

            print(prefill.format(split[1],split[2]))

if __name__ == "__main__":
    print("This will take a while (maybe 5-10 mins?), it gets faster as it goes though!")
    validateSetInfo()    
    generateTeamList()
    generateH2Hfiles()
    # Various utility functions that aren't needed to be run in most cases.
    # generateMoveList()
    # generateMoveCounts()
    # generateTypeEffectivenessCode()