#! python3
# This file defines the algorithms that are used to calculate the goals scored by each side during a fixture,
# as well as the outcomes of penalty shoot-outs


import random

# Define factors for scoring algorithm
HOME_ADV_FACTOR = 1.2
AWAY_ADV_FACTOR = 0.8


def random_factor():
    # return random decimal between 0 and 1
    return random.randrange(0, 100)/100


def home_goals(Team):
    # algorithm for goals scored by home team
    return round(random_factor() * HOME_ADV_FACTOR * Team.strength_factor * Team.last_game_factor() * Team.form_factor())


def away_goals(Team):
    # algorithm for goals scored by away team
    return round(random_factor() * AWAY_ADV_FACTOR * Team.strength_factor * Team.last_game_factor() * Team.form_factor())


def neutral_goals(Team):
    # algorithm for goals scored at neutral venue
    return round(random_factor() * Team.strength_factor * Team.last_game_factor() * Team.form_factor())


# Define coefficient calculation factors for group stage
GROUP_WIN_FACTOR = 3
GROUP_DRAW_FACTOR = 2
GROUP_LOSS_FACTOR = 1
GROUP_GOAL_FACTOR = 0.5


# Define scoring algorithm for a group fixture
def group_result(home_team, away_team):
    home_scored = home_goals(home_team)
    away_scored = away_goals(away_team)
    print(home_team.name + ' ' + str(home_scored) + '-' + str(away_scored) + ' ' + away_team.name)
    # Update stats
    home_team.played_season += 1
    home_team.goals_for_season += home_scored
    home_team.goals_against_season += away_scored
    home_team.goal_difference_season += home_scored - away_scored
    away_team.played_season += 1
    away_team.goals_for_season += away_scored
    away_team.goals_against_season += home_scored
    away_team.goal_difference_season += away_scored - home_scored
    if home_scored > away_scored:
        home_team.won_season += 1
        home_team.points_season += 3
        home_team.results.append(3)
        home_team.coefficient_season += GROUP_WIN_FACTOR + (home_scored * GROUP_GOAL_FACTOR)
        away_team.lost_season += 1
        away_team.results.append(0)
        away_team.coefficient_season += GROUP_LOSS_FACTOR + (away_scored * GROUP_GOAL_FACTOR)
    elif home_scored < away_scored:
        home_team.lost_season += 1
        home_team.results.append(0)
        home_team.coefficient_season += GROUP_LOSS_FACTOR + (home_scored * GROUP_GOAL_FACTOR)
        away_team.won_season += 1
        away_team.points_season += 3
        away_team.results.append(3)
        away_team.coefficient_season += GROUP_WIN_FACTOR + (away_scored * GROUP_GOAL_FACTOR)
    elif home_scored == away_scored:
        home_team.drawn_season += 1
        home_team.points_season += 1
        home_team.results.append(1)
        home_team.coefficient_season += GROUP_DRAW_FACTOR + (home_scored * GROUP_GOAL_FACTOR)
        away_team.drawn_season += 1
        away_team.points_season += 1
        away_team.results.append(1)
        away_team.coefficient_season += GROUP_DRAW_FACTOR + (away_scored * GROUP_GOAL_FACTOR)
    else:
        print('Unexpected match outcome')


# Define scoring algorithm for a knockout fixture
def knockout_result(team1, team2, scoring_method1, scoring_method2, win_factor, loss_factor, goal_factor, winners):
    team1_scored = scoring_method1(team1)
    team2_scored = scoring_method2(team2)
    print(team1.name + ' ' + str(team1_scored) + '-' + str(team2_scored) + ' ' + team2.name)
    # Update stats
    team1.played_season += 1
    team1.goals_for_season += team1_scored
    team1.goals_against_season += team2_scored
    team1.goal_difference_season += team1_scored - team2_scored
    team2.played_season += 1
    team2.goals_for_season += team2_scored
    team2.goals_against_season += team1_scored
    team2.goal_difference_season += team2_scored - team1_scored
    if team1_scored > team2_scored:
        team1.won_season += 1
        team2.lost_season += 1
        team1.results.append(3)
        team2.results.append(0)
        team1.coefficient_season += win_factor + (team1_scored * goal_factor)
        team2.coefficient_season += loss_factor + (team2_scored * goal_factor)
        winner = team1
    elif team1_scored < team2_scored:
        team1.lost_season += 1
        team2.won_season += 1
        team1.results.append(0)
        team2.results.append(3)
        team1.coefficient_season += loss_factor + (team1_scored * goal_factor)
        team2.coefficient_season += win_factor + (team2_scored * goal_factor)
        winner = team2
    elif team1_scored == team2_scored:
        team1.drawn_season += 1
        team2.drawn_season += 1
        team1.results.append(1)
        team2.results.append(1)
        # Winner decided by penalties
        winner = penalties('qf', team1, team2, team1_scored, team2_scored)
    else:
        print('Unexpected match outcome')
    winners.append(winner)


def penalty():
    # 75% chance of scoring
    return 1 if random.randrange(0, 100) > 25 else 0


# Define coefficient calculation factors for penalty shoot_outs
QF_PEN_WIN_FACTOR = 3.5
QF_PEN_LOSS_FACTOR = 2.5
QF_GOAL_FACTOR = 0.75
SF_PEN_WIN_FACTOR = 4
SF_PEN_LOSS_FACTOR = 3
SF_GOAL_FACTOR = 1
F_PEN_WIN_FACTOR = 6
F_PEN_LOSS_FACTOR = 4
F_GOAL_FACTOR = 2


# Define penalty shootout structure
def penalties(stage, team1, team2, team1_scored, team2_scored):
    # Defining the coefficient calculations for various knock-out stage penalty shootout outcomes
    if stage == 'qf':
        pen_win_factor = QF_PEN_WIN_FACTOR
        pen_loss_factor = QF_PEN_LOSS_FACTOR
        goals_factor = QF_GOAL_FACTOR
    elif stage == 'sf':
        pen_win_factor = SF_PEN_WIN_FACTOR
        pen_loss_factor = SF_PEN_LOSS_FACTOR
        goals_factor = SF_GOAL_FACTOR
    elif stage == 'f':
        pen_win_factor = F_PEN_WIN_FACTOR
        pen_loss_factor = F_PEN_LOSS_FACTOR
        goals_factor = F_GOAL_FACTOR
    else:
        print('Unexpected tournament stage')

    # Calculating the penalty shootout scores after 5 penalties each
    team1pens = 0
    team2pens = 0
    pens_left = [5, 5]
    for i in range(0, 5):
        team1pen = penalty()
        if team1pen == 1:
            team1pens += 1
        else:
            pass
        pens_left[0] -= 1
        if team1pens - team2pens > pens_left[1]:
            break
        elif (team2pens - team1pens) > pens_left[0]:
            break
        else:
            team2pen = penalty()
            if team2pen == 1:
                team2pens += 1
            else:
                pass
            pens_left[1] -= 1
            if team1pens - team2pens > pens_left[1]:
                break
            elif team2pens - team1pens > pens_left[0]:
                break
            else:
                continue

    # Calculating the sudden death results if the penalty shootout is tied after 5 penalties each
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
        team1.coefficient_season += pen_win_factor + (team1_scored * goals_factor)
        team2.coefficient_season += pen_loss_factor + (team2_scored * goals_factor)
        winner = team1
    elif team2pens > team1pens:
        print('* ' + team2.name + ' won ' + str(team2pens) + '-' + str(team1pens) + ' on pens')
        team1.coefficient_season += pen_loss_factor + (team1_scored * goals_factor)
        team2.coefficient_season += pen_win_factor + (team2_scored * goals_factor)
        winner = team2
    return winner
