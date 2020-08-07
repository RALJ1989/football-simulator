#! python3
# This file defines the algorithms that are used to determine any updates to properties of squads

import math

# Define the cost of buying or selling 1 unit of squad strength
COST_TO_BUY_SELL = 12
WAGES_PER_UNIT = 2


def update_team_strength(final_teams_ranking):
    for t in final_teams_ranking:
        # Deduct wages from bank
        t.bank -= t.wages
        # Calculate whether the team needs to buy, sell or maintain squad strength given its finances
        change_in_strength = math.floor(t.bank / (COST_TO_BUY_SELL + WAGES_PER_UNIT)) if t.bank < 0 else 0 \
            if t.bank == 0 else 0 \
            if t.bank < t.bank_reserve else math.floor((t.bank - t.bank_reserve) / (COST_TO_BUY_SELL + WAGES_PER_UNIT))
        # Calculate the cost of any necessary changes
        cost_update = -change_in_strength * COST_TO_BUY_SELL if change_in_strength < 0 \
            else -change_in_strength * COST_TO_BUY_SELL
        # Update the bank balance after these costs have been taken into account
        t.bank += cost_update
        # Update the squad strength with the prior changes
        t.strength2 = t.strength1 + change_in_strength


def update_squads(team_header_width, final_teams_ranking):
    print('   Team' + ' '*(team_header_width - 3) + 'Strength ' + 'Change')
    final_teams_ranking = sorted(final_teams_ranking, key=lambda team: team.strength2, reverse=True)
    rank = 1
    for t in final_teams_ranking:
        strength_change = t.strength2 - t.strength1
        print(str(rank) + ' '*(2 - len(str(rank))),
              t.name + ' '*(team_header_width - len(t.name)),
              str(t.strength2) + ' '*(8 - len(str(t.strength2))),
              strength_change if strength_change < 0 else '+' + str(strength_change) if strength_change > 0 else 0)
        rank += 1


def reset_season_stats(teams):
    for t in teams:
        t.played_forever += t.played_season
        t.won_forever += t.won_season
        t.drawn_forever += t.drawn_season
        t.lost_forever += t.lost_season
        t.goals_for_forever += t.goals_for_season
        t.goals_against_forever += t.goals_against_season
        t.goal_difference_forever += t.goal_difference_season
        t.points_forever += t.points_season
        t.coefficient_forever += t.coefficient_season
        t.prize_money_forever += t.prize_money_season
        t.strength1 = t.strength2
        t.strength_factor = 1.0 + ((t.strength1 - 5) / 5.0)
        t.wages = t.strength1 * 2
        t.bank_reserve = math.ceil(t.wages * 0.25)
        t.bank = t.bank
        t.played_season = 0
        t.won_season = 0
        t.drawn_season = 0
        t.lost_season = 0
        t.goals_for_season = 0
        t.goals_against_season = 0
        t.goal_difference_season = 0
        t.points_season = 0
        t.results = [0, 0, 1.5, 5, 1]
        t.coefficient_season = 0
        t.prize_money_season = 0
