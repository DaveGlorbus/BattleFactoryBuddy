# Semi-replacement for Team.py. No need to create and object for a bunch of this
from collections import Counter
import math

class StaticTeamUtils:

    # Note this doesn't check team validity, that needs to be done ahead of itme.
    @staticmethod 
    def getTeamInfo(setA, setB, setC):

        # Sort out Style
        stylepoints = ""
        for set in [setA,setB,setC]:
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
            style = 8
        elif t7 == 1:
            style = 7
        elif t6 == 1:
            style = 6
        elif t5 == 1:
            style = 5
        elif t4 == 1:
            style = 4
        elif t3 == 1:
            style = 3
        elif t2 == 1:
            style = 2
        elif t1 == 1:
            style = 1
        else:
            style = 0

        # Sort out Type
        types = []
        for set in [setA, setB, setC]:
            types += set.types
        maxcount = 0

        for a in types:            
            if a == "":
                continue
            number = types.count(a)
            if number > maxcount:
                maxcount = number
                type = a
            elif number == maxcount:
                if a != type:
                    type = "None"
        return (type, style)
