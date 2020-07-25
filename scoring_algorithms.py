#! python3

import random

# Define factors for scoring algorithm
homeAdvFactor = 1.2
awayAdvFactor = 0.8


def random_factor():
    # return random decimal between 0 and 1
    return random.randrange(0, 100)/100


def home_goals(Team):
    # algorithm for goals scored by home team
    return round(random_factor() * homeAdvFactor * Team.strengthFactor * Team.lastGameFactor() * Team.formFactor())


def away_goals(Team):
    # algorithm for goals scored by away team
    return round(random_factor() * awayAdvFactor * Team.strengthFactor * Team.lastGameFactor() * Team.formFactor())


def neutral_goals(Team):
    # algorithm for goals scored at neutral venue
    return round(random_factor() * Team.strengthFactor * Team.lastGameFactor() * Team.formFactor())


def penalty():
    # 75% chance of scoring
    return 1 if random.randrange(0, 100) > 25 else 0


# Define penalty shootout structure
def penalties(stage, team1, team2, team1goals, team2goals):
    if stage == 'qf':
        win_pen_factor = 3.5
        lose_pen_factor = 2.5
        goals_factor = 0.75
    elif stage == 'sf':
        win_pen_factor = 4
        lose_pen_factor = 3
        goals_factor = 1
    elif stage == 'fin':
        win_pen_factor = 6
        lose_pen_factor = 4
        goals_factor = 2
    else:
        print('Unexpected tournament stage')

    global winner
    winner = 0
    team1pens = 0
    team2pens = 0
    for i in range(0, 5):
        team1pen = penalty()
        team2pen = penalty()
        if team1pen == 1:
            team1pens += 1
        else:
            continue
        if team2pen == 1:
            team2pens += 1
        else:
            continue
    if team1pens > team2pens:
        print('* ' + team1.name + ' won ' + str(team1pens) + '-' + str(team2pens) + ' on pens')
        team1.coefficient += win_pen_factor + (team1goals * goals_factor)
        team2.coefficient += lose_pen_factor + (team2goals * goals_factor)
        winner = team1
    elif team2pens > team1pens:
        print('* ' + team2.name + ' won ' + str(team2pens) + '-' + str(team1pens) + ' on pens')
        team1.coefficient += lose_pen_factor + (team1goals * goals_factor)
        team2.coefficient += win_pen_factor + (team2goals * goals_factor)
        winner = team2
    else:
        while team1pens == team2pens:
            team1pen = penalty()
            team2pen = penalty()
            if team1pen == 1:
                team1pens += 1
            else:
                continue
            if team2pen == 1:
                team2pens += 1
            else:
                continue
        if team1pens > team2pens:
            print('* ' + team1.name + ' won ' + str(team1pens) + '-' + str(team2pens) + ' on pens')
            team1.coefficient += win_pen_factor + (team1goals * goals_factor)
            team2.coefficient += lose_pen_factor + (team2goals * goals_factor)
            winner = team1
        elif team2pens > team1pens:
            print('* ' + team2.name + ' won ' + str(team2pens) + '-' + str(team1pens) + ' on pens')
            team1.coefficient += lose_pen_factor + (team1goals * goals_factor)
            team2.coefficient += win_pen_factor + (team2goals * goals_factor)
            winner = team2
    return winner
