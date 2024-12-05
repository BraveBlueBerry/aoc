import re

i = open("input.txt", "r")

leftlist = []
rightlist = []

for line in i:
    matches = re.findall("\d{1,5}", line)
    leftlist.append(matches[0])
    rightlist.append(matches[1])

leftlist.sort()
rightlist.sort()


total = 0

for x in range(len(leftlist)):
    distance = abs(int(rightlist[x]) - int(leftlist[x]))
    total += distance

print(total)