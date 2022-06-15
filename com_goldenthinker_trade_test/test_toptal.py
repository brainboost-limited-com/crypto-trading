
import re

regex = r"[a-z,A-Z]+"

test_str = ("T[0] = \"test14a\"  R[0] = \"Wrong answer\"\n"
	"T[1] = \"test2\"   R[1] = \"OK\"\n"
	"T[2] = \"test145b\"  R[2] = \"Runtime error\"\n"
	"T[3] = \"test1c\"  R[3] = \"OK\"")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
