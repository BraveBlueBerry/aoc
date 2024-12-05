import re
from copy import copy

i = open("input_small.txt", "r")

reports = []

for line in i:
    matches = re.findall("\d{1,5}", line)
    report = []
    for match in matches:
        report.append(int(match))
    reports.append(report)

safeReports = 0
unsafereports = []

def is_report_safe(r, problemDampener, depth=0):
    should_be_increasing = r[1] > r[0]
    isSafe = True
    for i in range(len(r) - 1):
        diff = abs(r[i + 1] - r[i])
        if diff < 1 or diff > 3:
            isSafe = False
        if r[i + 1] < r[i] and should_be_increasing:
            isSafe = False
        if r[i + 1] > r[i] and not should_be_increasing:
            isSafe = False

        if (not isSafe) and problemDampener:
            new_report = copy(r)
            new_report.pop(i)
            new_report_2 = copy(r)
            new_report_2.pop(i+1)

            if i == 1:
                new_report_0 = copy(r)
                new_report_0.pop(0)
                return is_report_safe(new_report, False, depth + 1) or is_report_safe(new_report_2, False, depth + 2) or is_report_safe(new_report_0, False, depth + 3)

            return is_report_safe(new_report, False, depth + 1) or is_report_safe(new_report_2, False, depth + 2)


    return isSafe


for report in reports:
    isSafe = is_report_safe(report, True)
    if not isSafe:
        unsafereports.append(report)

    if isSafe:
        safeReports += 1

print(f"Number of safe reports: {safeReports}")