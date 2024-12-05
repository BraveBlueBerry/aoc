import re

input = open("input.txt", "r")

leftlist = []
rightlist = []

for line in input:
    matches = re.findall("\d{1,5}", line)
    leftlist.append(matches[0])
    rightlist.append(matches[1])

input.close()
total = 0

for x in leftlist:
    total += int(x) * rightlist.count(x)

print(total)