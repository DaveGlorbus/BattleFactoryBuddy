from collections import Counter
import math

# A class representing a team of 3 sets. This is used to work out what phrase / style / round a team could be in. As 
# such it's not used at calculation time as that's all precomputed to try and speed up the queries. During calculation
# we just use a flat list of uids of sets to save on memory usage rather than wrapping in an object.
class Team:
    def __init__(self, set1, set2, set3):
        self.sets = [set1, set2, set3]
        self.style = "99"
        self.type = ""

        self.initCalculateStyle()
        self.initCalculateType()
        self.initCalculateRound()

    # Work out which style this team has. Called during init.
    # ALTSETS - Edits required if your calculation of scientist hint for styles is different.
    def initCalculateStyle(self):
        stylepoints = ""
        for set in self.sets:
            stylepoints += set.moves
        
        counter = Counter(stylepoints)
        t1 = 1 if (counter["1"] > 2) else 0
        t2 = 1 if (counter["2"] > 2) else 0
        t3 = 1 if (counter["3"] > 2) else 0
        t4 = 1 if (counter["4"] > 1) else 0
        t5 = 1 if (counter["5"] > 1) else 0
        t6 = 1 if (counter["6"] > 1) else 0
        t7 = 1 if (counter["7"] > 1) else 0

        if (t1 + t2 + t3 + t4 + t5 + t6 + t7) > 2:
            self.style = 8
        elif t7 == 1:
            self.style = 7
        elif t6 == 1:
            self.style = 6
        elif t5 == 1:
            self.style = 5
        elif t4 == 1:
            self.style = 4
        elif t3 == 1:
            self.style = 3
        elif t2 == 1:
            self.style = 2
        elif t1 == 1:
            self.style = 1
        else:
            self.style = 0

    # Calculate the type covered by the team.
    # ALTSETS - Edits required if your calculation of scientist hint for types is different.
    def initCalculateType(self):
        
        types = []
        for set in self.sets:
            types += set.types
        maxcount = 0

        for a in types:            
            if a == "":
                continue
            number = types.count(a)
            if number > maxcount:
                maxcount = number
                self.type = a
            elif number == maxcount:
                if a != self.type:
                    self.type = "None"

    # Work out which "round" this team can appear in. This isn't 1-1 with rounds in the game but more like buckets.
    # 1 = round 1
    # 2 = round 2
    # 3 = round 3
    # 4 = round 1 or 2    
    # ALTSETS - Edits required if your sets maps to rounds in different ways.
    def initCalculateRound(self):
        roundmarkers = []
        for monset in self.sets:
            roundmarkers.append(int(monset.roundInfo))        
        roundmarkers.sort()
        roundmarkers = set(roundmarkers)        

        # At least one 1, and any number of other 1s, 2s.  - Round 1        
        if roundmarkers in ({1}, {1,2}):
            self.round = "1"
        # At least one 3, and any number of other 2s, 3s - Round 2
        elif roundmarkers in ({3}, {2,3}):
            self.round = "2"
        # Only 4s - Round 3
        elif roundmarkers == {4}:
            self.round = "3"
        # 2s only - Round 1 or 2
        elif roundmarkers == {2}:
            self.round = "4"
        else:
            self.round = "0"  
        
    # Return a human readable list of the sets in the team.
    def readableStr(self):
        return (
            self.sets[0].id
            + ","
            + self.sets[1].id
            + ","
            + self.sets[2].id
            + ","
            + self.round
        )
    
    # Return the uids of the Sets in the team.
    def shortStr(self):
        return (
            str(self.sets[0].uid)
            + ","
            + str(self.sets[1].uid)
            + ","
            + str(self.sets[2].uid)
            + ","
            + self.round
        )

    # Used to return the type and phrase for a team. Used for team phrase analysis.
    def phraseoutput(self):
        typstr = ""
        phrasestr = "The favourite battle style "
        if self.type == "None":
            typstr = (
                "The Trainer appears to have no clear favourites when it comes to type."
            )
        else:
            typstr = (
                "The Trainer is apparently skilled in the handling of the %s type."
                % (self.type)
            )
        if self.style == 0:
            phrasestr += "appears to be free-spirited and unrestrained."
        elif self.style == 1:
            phrasestr += "appears to be one based on total preparation."
        elif self.style == 2:
            phrasestr += "appears to be slow and steady."
        elif self.style == 3:
            phrasestr += "appears to be one of endurance."
        elif self.style == 4:
            phrasestr += "appears to be high risk, high return."
        elif self.style == 5:
            phrasestr += "appears to be weakening the foe to start."
        elif self.style == 6:
            phrasestr += "appears to be impossible to predict."
        elif self.style == 7:
            phrasestr += "appears to depend on the battle's flow."
        elif self.style == 8:
            phrasestr += "appears to be flexibly adaptable to the situation."
        return (typstr, phrasestr)
