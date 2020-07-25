#! python3

# Define the league table layout
leagueHeader = '        | STR  | PL  | W   | D   | L   | GF  | GA  | GD  | PTS'

# Define group table format
def groups_table(sortedGroups, groupNames, desiredLength):
    groupIndex = 0
    for g in sortedGroups:
        print('\n' + str.upper(groupNames[groupIndex]) + ' ' + leagueHeader)
        for t in g:
            leagueRow = t.name + str(' ')*(desiredLength-len(t.name)) + '| ' + str(t.strength1) + str(' ')*(5-len(str(t.strength1))) \
                        + '| ' + str(t.pl) + str(' ')*(4-len(str(t.pl))) + '| ' + str(t.w) + str(' ')*(4-len(str(t.w))) \
                        + '| ' + str(t.d) + str(' ')*(4-len(str(t.d))) + '| ' + str(t.l) + str(' ')*(4-len(str(t.l))) \
                        + '| ' + str(t.gf) + str(' ')*(4-len(str(t.gf))) + '| ' + str(t.ga) + str(' ')*(4-len(str(t.ga))) \
                        + '| ' + str(t.gd) + str(' ')*(4-len(str(t.gd))) + '| ' + str(t.pts) + str(' ')*(4-len(str(t.pts)))
            print(leagueRow)
        if groupIndex ==3:
            continue
        else:
            groupIndex += 1
    return
