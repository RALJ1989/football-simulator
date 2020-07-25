#! python3

import random
from scoring_algorithms import random_factor, home_goals, away_goals, neutral_goals, penalty, penalties
from group_structure import groups_table


# Define 'Team' class, which contains team name and team strength
class Team:
    def __init__(self, name, strength1):
        self.name = name
        self.strength1 = strength1
        self.strengthFactor = 0.3 + (self.strength1 / 7.5)
        self.pl = 0
        self.w = 0
        self.d = 0
        self.l = 0
        self.gf = 0
        self.ga = 0
        self.gd = 0
        self.pts = 0
        self.results = [0, 0, 1.5, 5, 1]
        self.coefficient = 0

    @property
    def formPoints(self):
        return sum(self.results[-5:])
    def formFactor(self):
        return 0.7 + 0.6 * (self.formPoints / 15)
    def lastGameFactor(self):
        return 0.6 + (0.8 if self.results[-1] == 3 else 0.4 if self.results[-1] == 1 else 0)
    def strengthEq(self):
        topCoeff = 55
        topCoeffStrength = 20
        highCoeff = 35
        highCoeffStrength = 15
        lowCoeff = 6
        lowCoeffStrength = 5
        return topCoeffStrength if self.coefficient > topCoeff else \
            (highCoeffStrength + (((self.coefficient - highCoeff)/(topCoeff - highCoeff))*(topCoeffStrength - highCoeffStrength))) \
                if self.coefficient > highCoeff else \
                lowCoeffStrength + (((self.coefficient - lowCoeff)/(highCoeff - lowCoeff))*(highCoeffStrength - lowCoeffStrength))
    def strength2(self):
        return round(2*(self.strength1 + ((self.strengthEq() - self.strength1)/10)), 0)/2


# Define the initial team names and strengths
liverpool = Team("Liverpool", 19)
man_city = Team("Man City", 17)
chelsea = Team("Chelsea", 15)
leicester = Team("Leicester", 13)
man_utd = Team("Man Utd", 14)
wolves = Team("Wolves", 11)
sheffield_utd = Team("Sheffield Utd", 10)
tottenham = Team("Tottenham", 14)
arsenal = Team("Arsenal", 13)
burnley = Team("Burnley", 10)
everton = Team("Everton", 11)
southampton = Team("Southampton", 9)
newcastle = Team("Newcastle", 8)
crystal_palace = Team("Crystal Palace", 8)
west_ham = Team("West Ham", 8)
watford = Team("Watford",7)
# brighton = Team("Brighton", 6)
# bournemouth = Team("Bournemouth", 6)
# aston_villa = Team("Aston Villa", 6)
# norwich = Team("Norwich", 5)

# Define a list of all the teams
teams = [liverpool, man_city, chelsea, leicester, man_utd, wolves, sheffield_utd,
         tottenham, arsenal, burnley, everton, southampton, newcastle, crystal_palace,
         west_ham, watford]
sortTeams = sorted(teams, key=lambda team: (-team.strength1, team.name), reverse=False)

# Create an (initially empty) list of winners
tournamentWinners = []

for i in range(99):
    # Sort all teams randomly
    random.shuffle(sortTeams)

    # Split shuffled teams into groups
    groupA = sortTeams[0:4]
    groupB = sortTeams[4:8]
    groupC = sortTeams[8:12]
    groupD = sortTeams[12:16]
    allGroups = [groupA, groupB, groupC, groupD]
    groupNames = ['Group A', 'Group B', 'Group C', 'Group D']

    # Display Groups
    groupIndex = 0
    for g in allGroups:
        groupTeamNames = []
        print(groupNames[groupIndex] + ': ' + ', '.join(t.name for t in g))
        groupIndex += 1

    # Find the max length of team names and define team name column width
    sortTeamsString = []
    for t in sortTeams:
        sortTeamsString.append(t.name)
    maxLength = len(max(sortTeamsString, key=len))
    desiredLength = maxLength + 2

    # Sort groups
    tableSort = lambda team: (team.pts, (team.gd, (-team.strength1, team.name)))
    sortedGroupA = sorted(groupA, key=tableSort, reverse=True)
    sortedGroupB = sorted(groupB, key=tableSort, reverse=True)
    sortedGroupC = sorted(groupC, key=tableSort, reverse=True)
    sortedGroupD = sorted(groupD, key=tableSort, reverse=True)
    sortedGroups = [sortedGroupA, sortedGroupB, sortedGroupC, sortedGroupD]

    # Show group tables
    groups_table(sortedGroups, groupNames, desiredLength)

    # Generate fixtures and scores
    matchdays = ['Matchday 1', 'Matchday 2', 'Matchday 3', 'Matchday 4', 'Matchday 5', 'Matchday 6']
    matchdayFixtures = [[[0, 1], [2, 3]], [[3, 0], [1, 2]], [[0, 2], [1, 3]], [[2, 0], [3, 1]], [[1, 0], [3, 2]], [[0, 3], [2, 1]]]
    matchdayReference = 0
    for m in matchdays:
        print('\n' + matchdays[matchdayReference] + ':')
        groupIndex = 0
        for g in allGroups:
            print('\n' + groupNames[groupIndex] + ' fixtures:')
            for f in range(len(matchdayFixtures[matchdayReference])):
                homeTeam = allGroups[groupIndex][matchdayFixtures[matchdayReference][f][0]]
                awayTeam = allGroups[groupIndex][matchdayFixtures[matchdayReference][f][1]]
                # Fixtures
                print(homeTeam.name + ' vs ' + awayTeam.name)
                # Scores
                homeGoals = home_goals(homeTeam)
                awayGoals = away_goals(awayTeam)
                print(homeTeam.name + ' ' + str(homeGoals) + '-' + str(awayGoals) + ' ' + awayTeam.name)
                # Update stats
                homeTeam.pl += 1
                homeTeam.gf += homeGoals
                homeTeam.ga += awayGoals
                homeTeam.gd += homeGoals - awayGoals
                awayTeam.pl += 1
                awayTeam.gf += awayGoals
                awayTeam.ga += homeGoals
                awayTeam.gd += awayGoals - homeGoals
                if homeGoals > awayGoals:
                    homeTeam.w += 1
                    homeTeam.pts += 3
                    homeTeam.results.append(3)
                    homeTeam.coefficient += 3 + (homeGoals * 0.5)
                    awayTeam.l += 1
                    awayTeam.results.append(0)
                    awayTeam.coefficient += 1 + (awayGoals * 0.5)
                elif homeGoals < awayGoals:
                    homeTeam.l += 1
                    homeTeam.results.append(0)
                    homeTeam.coefficient += 1 + (homeGoals * 0.5)
                    awayTeam.w += 1
                    awayTeam.pts += 3
                    awayTeam.results.append(3)
                    awayTeam.coefficient += 3 + (awayGoals * 0.5)
                elif homeGoals == awayGoals:
                    homeTeam.d += 1
                    homeTeam.pts += 1
                    homeTeam.results.append(1)
                    homeTeam.coefficient += 2 + (homeGoals * 0.5)
                    awayTeam.d += 1
                    awayTeam.pts += 1
                    awayTeam.results.append(1)
                    awayTeam.coefficient += 2 + (awayGoals * 0.5)
                else:
                    print('Unexpected match outcome')
            groupIndex += 1
        matchdayReference += 1

    # Final sort and display group tables
    sortedGroupA = sorted(groupA, key=tableSort, reverse=True)
    sortedGroupB = sorted(groupB, key=tableSort, reverse=True)
    sortedGroupC = sorted(groupC, key=tableSort, reverse=True)
    sortedGroupD = sorted(groupD, key=tableSort, reverse=True)
    sortedGroups = [sortedGroupA, sortedGroupB, sortedGroupC, sortedGroupD]

    groups_table(sortedGroups, groupNames, desiredLength)

    # Quarter-final fixtures
    qF1 = [sortedGroupA[0], sortedGroupC[1]]
    qF2 = [sortedGroupB[0], sortedGroupD[1]]
    qF3 = [sortedGroupC[0], sortedGroupA[1]]
    qF4 = [sortedGroupD[0], sortedGroupB[1]]
    quarterFinals = [qF1, qF2, qF3, qF4]

    quarterFinalNumber = 1
    quarterFinalRef = 0
    quarterFinalWinners = []
    for q in quarterFinals:
        team1 = quarterFinals[quarterFinalRef][0]
        team2 = quarterFinals[quarterFinalRef][1]
        # Fixture
        print('\n' + 'Quarter-final ' + str(quarterFinalNumber) + ':\n' + team1.name + ' vs ' + team2.name)
        # Score
        team1goals = home_goals(team1)
        team2goals = away_goals(team2)
        print(team1.name + ' ' + str(team1goals) + '-' + str(team2goals) + ' ' + team2.name)
        # Update stats
        if team1goals > team2goals:
            team1.results.append(3)
            team2.results.append(0)
            team1.coefficient += 4.5 + (team1goals * 0.75)
            team2.coefficient += 1.5 + (team2goals * 0.75)
            winner = team1
        elif team1goals < team2goals:
            team1.results.append(0)
            team2.results.append(3)
            team1.coefficient += 1.5 + (team1goals * 0.75)
            team2.coefficient += 4.5 + (team2goals * 0.75)
            winner = team2
        elif team1goals == team2goals:
            team1.results.append(1)
            team2.results.append(1)
            # winner decided by penalties
            winner = penalties('qf', team1, team2, team1goals, team2goals)
        else:
            print('Unexpected match outcome')
        quarterFinalWinners.append(winner)
        quarterFinalNumber += 1
        quarterFinalRef += 1

    print('\nQuarter-final winners:\n' + ', '.join(w.name for w in quarterFinalWinners))

    # Semi-final fixtures
    sF1 = [quarterFinalWinners[0], quarterFinalWinners[1]]
    sF2 = [quarterFinalWinners[2], quarterFinalWinners[3]]
    semiFinals = [sF1, sF2]

    semiFinalNumber = 1
    semiFinalRef = 0
    semiFinalWinners = []
    for s in semiFinals:
        team1 = semiFinals[semiFinalRef][0]
        team2 = semiFinals[semiFinalRef][1]
        # Fixture
        print('\n' + 'Semi-final ' + str(semiFinalNumber) + ':\n' + team1.name + ' vs ' + team2.name)
        # Score
        team1goals = neutral_goals(team1)
        team2goals = neutral_goals(team2)
        print(team1.name + ' ' + str(team1goals) + '-' + str(team2goals) + ' ' + team2.name)
        # Update stats
        if team1goals > team2goals:
            team1.results.append(3)
            team2.results.append(0)
            team1.coefficient += 5 + (team1goals * 1)
            team2.coefficient += 2 + (team2goals * 1)
            winner = team1
        elif team1goals < team2goals:
            team1.results.append(0)
            team2.results.append(3)
            team1.coefficient += 2 + (team1goals * 1)
            team2.coefficient += 5 + (team2goals * 1)
            winner = team2
        elif team1goals == team2goals:
            team1.results.append(1)
            team2.results.append(1)
            # winner decided by penalties
            winner = penalties('sf', team1, team2, team1goals, team2goals)
        else:
            print('Unexpected match outcome')
        semiFinalWinners.append(winner)
        semiFinalNumber += 1
        semiFinalRef += 1

    print('\nSemi-final winners:\n' + ', '.join(w.name for w in semiFinalWinners))

    # Final fixture
    team1 = semiFinalWinners[0]
    team2 = semiFinalWinners[1]

    print('\nFinal:\n' + team1.name + ' vs ' + team2.name)

    # Final score
    team1goals = neutral_goals(team1)
    team2goals = neutral_goals(team2)
    print(team1.name + ' ' + str(team1goals) + '-' + str(team2goals) + ' ' + team2.name)

    # Update final stats
    if team1goals > team2goals:
        team1.results.append(3)
        team2.results.append(0)
        team1.coefficient += 7 + (team1goals * 2)
        team2.coefficient += 3 + (team2goals * 2)
        winner = team1
    elif team1goals < team2goals:
        team1.results.append(0)
        team2.results.append(3)
        team1.coefficient += 3 + (team1goals * 2)
        team2.coefficient += 7 + (team2goals * 2)
        winner = team2
    elif team1goals == team2goals:
        team1.results.append(1)
        team2.results.append(1)
        # winner decided by penalties
        winner = penalties('fin', team1, team2, team1goals, team2goals)
    else:
        print('Unexpected match outcome')

    # Print the winner of the final
    print('\nFinal winner:\n' + winner.name)

    # Update the list of tournament winners
    tournamentWinners.append(winner.name)

    # Rank the teams by tournament performance (based on coefficients)
    finalTeamsRanking = []
    for t in teams:
        finalTeamsRanking.append(t)
    finalTeamsRanking = sorted(finalTeamsRanking, key=lambda team: team.coefficient, reverse=True)
    print('\nFinal tournament rankings:')
    for t in finalTeamsRanking:
        print(t.name, t.coefficient)

    # Display the change in strength of each team based on tournament performance
    print('\nChanges in strength for next season:')
    for t in finalTeamsRanking:
        print(t.name, t.strength2(), t.strength2() - t.strength1)

    # Reset the stats for next season and update strengths
    for t in teams:
        t.strength1 = t.strength2()
        t.pl = 0
        t.w = 0
        t.d = 0
        t.l = 0
        t.gf = 0
        t.ga = 0
        t.gd = 0
        t.pts = 0
        t.results = [0, 0, 1.5, 5, 1]
        t.coefficient = 0

print('\nTournament winners:\n' + str(tournamentWinners))
