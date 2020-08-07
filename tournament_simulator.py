#! python3
# This file contains an engine for simulating the outcome of a 16-team football tournament and extrapolating 
# over multiple subsequent seasons

import random
import math
from scoring_algorithms import random_factor, home_goals, away_goals, neutral_goals, group_result, knockout_result, \
    penalty, penalties
from group_structure import groups_table, sort_groups
from squad_algorithms import update_team_strength, update_squads, reset_season_stats

# Define number of seasons to simulate
number_seasons = 1


# Define 'Team' class, which contains team name and team strength
class Team:
    def __init__(self, name, strength1):
        self.name = name
        self.strength1 = strength1
        self.strength2 = 0
        self.bank = int(strength1 / 1.5)
        self.wages = strength1 * 2
        self.bank_reserve = math.ceil(self.wages * 0.25)
        self.strength_factor = 1.0 + ((self.strength1 - 5) / 5.0)
        self.played_season = 0
        self.won_season = 0
        self.drawn_season = 0
        self.lost_season = 0
        self.goals_for_season = 0
        self.goals_against_season = 0
        self.goal_difference_season = 0
        self.points_season = 0
        self.results = [0, 0, 1.5, 5, 1]
        self.coefficient_season = 0
        self.prize_money_season = 0
        self.played_forever = 0
        self.won_forever = 0
        self.drawn_forever = 0
        self.lost_forever = 0
        self.goals_for_forever = 0
        self.goals_against_forever = 0
        self.goal_difference_forever = 0
        self.points_forever = 0
        self.coefficient_forever = 0
        self.prize_money_forever = 0

    @property
    def recent_form(self):
        return sum(self.results[-5:])

    def form_factor(self):
        return 0.6 + 0.8 * (self.recent_form / 15)

    def last_game_factor(self):
        return 0.6 + (0.8 if self.results[-1] == 3 else 0.4 if self.results[-1] == 1 else 0)


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

# Create an (initially empty) list of winners to be populated at the end of each season
tournamentWinners = []

# Find the max length of team names in order to define header width for team names
sort_teams_string = []
for t in sortTeams:
    sort_teams_string.append(t.name)
max_team_length = len(max(sort_teams_string, key=len))
team_header_width = max_team_length + 2

# Loop through simulation for each season
for i in range(number_seasons):
    print('SEASON ' + str(i+1) + ' BEGINS')
    # Sort all teams randomly
    random.shuffle(sortTeams)

    # Split shuffled teams into groups
    group_a = sortTeams[0:4]
    group_b = sortTeams[4:8]
    group_c = sortTeams[8:12]
    group_d = sortTeams[12:16]
    group_names = [[group_a, 'GROUP A'], [group_b, 'GROUP B'], [group_c, 'GROUP C'], [group_d, 'GROUP D']]

    # Display groups and calculate group of death
    print('\nThe draw has been made!\n')
    group_of_death = [0, 0]
    for g in group_names:
        group_strength = 0
        print(g[1] + ': ')
        for t in g[0]:
            print(t.name)
            group_strength += t.strength1
        print('')
        if group_strength > group_of_death[0]:
            group_of_death = [group_strength, g[1]]
        else:
            continue
    print('It looks like ' + str(group_of_death[1]) + ' is the group of death!')

    # Sort groups
    sorted_groups = sort_groups(group_a, group_b, group_c, group_d)

    # Show group tables
    groups_table(sorted_groups, team_header_width)

    # Group stage fixture format
    matchday_fixtures = [['Matchday 1', [0, 1], [2, 3]], ['Matchday 2', [3, 0], [1, 2]], ['Matchday 3', [0, 2], [1, 3]],
                 ['Matchday 4', [2, 0], [3, 1]], ['Matchday 5', [1, 0], [3, 2]], ['Matchday 6', [0, 3], [2, 1]]]

    # Generate fixtures and scores for group stage
    for m in matchday_fixtures:
        print('\n' + m[0] + ':')
        for g in sorted_groups:
            print('\n' + g[1] + ' fixtures:')
            for f in (m[1], m[2]):
                home_team = g[0][f[0]]
                away_team = g[0][f[1]]
                # Fixtures
                print(home_team.name + ' vs ' + away_team.name)
                # Scores
                group_result(home_team, away_team)

    # Sort the final group tables, then display them
    sorted_groups = sort_groups(group_a, group_b, group_c, group_d)
    groups_table(sorted_groups, team_header_width)

    global winner
    winner = 0

    # Define coefficient calculation factors for knockout rounds
    QF_WIN_FACTOR = 4.5
    QF_LOSS_FACTOR = 1.5
    QF_GOAL_FACTOR = 0.75
    SF_WIN_FACTOR = 5
    SF_LOSS_FACTOR = 2
    SF_GOAL_FACTOR = 1
    F_WIN_FACTOR = 7
    F_LOSS_FACTOR = 3
    F_GOAL_FACTOR = 2

    # Quarter-final fixture format
    qF1 = [sorted_groups[0][0][0], sorted_groups[2][0][1]]
    qF2 = [sorted_groups[1][0][0], sorted_groups[3][0][1]]
    qF3 = [sorted_groups[2][0][0], sorted_groups[0][0][1]]
    qF4 = [sorted_groups[3][0][0], sorted_groups[1][0][1]]
    quarter_finals = [[qF1, 1], [qF2, 2], [qF3, 3], [qF4, 4]]
    quarter_final_winners = []

    # Generate fixtures and scores for quarter-finals
    for q in quarter_finals:
        team1 = q[0][0]
        team2 = q[0][1]
        # Fixtures
        print('\n' + 'Quarter-final ' + str(q[1]) + ':\n' + team1.name + ' vs ' + team2.name)
        # Scores
        knockout_result(team1, team2, home_goals, away_goals, QF_WIN_FACTOR,
                        QF_LOSS_FACTOR, QF_GOAL_FACTOR, quarter_final_winners)

    # Display a summary of the quarter-final winners
    print('\nQuarter-final summary:\n' + ', '.join(w.name.upper() for w in quarter_final_winners[:3]) +
          ' and ' + quarter_final_winners[3].name.upper() + ' have made it to the Semi-finals!')

    # Semi-final fixture format
    sF1 = [quarter_final_winners[0], quarter_final_winners[1]]
    sF2 = [quarter_final_winners[2], quarter_final_winners[3]]
    semiFinals = [[sF1, 1], [sF2, 2]]
    semi_final_winners = []

    # Generate fixtures and scores for semi-finals
    for s in semiFinals:
        team1 = s[0][0]
        team2 = s[0][1]
        # Fixtures
        print('\n' + 'Semi-final ' + str(s[1]) + ':\n' + team1.name + ' vs ' + team2.name)
        # Scores
        knockout_result(team1, team2, neutral_goals, neutral_goals, SF_WIN_FACTOR,
                        SF_LOSS_FACTOR, SF_GOAL_FACTOR, semi_final_winners)

    # Display a summary of the semi-final winners
    print('\nSemi-final summary:\n' + ' and '
          .join(w.name.upper() for w in semi_final_winners) +
          ' have made it to the Final!')

    # Final fixture format
    team1 = semi_final_winners[0]
    team2 = semi_final_winners[1]
    final_winner = []

    # Print final fixture
    print('\nFinal:\n' + team1.name + ' vs ' + team2.name)

    # Generate result for final
    knockout_result(team1, team2, neutral_goals, neutral_goals, F_WIN_FACTOR,
                    F_LOSS_FACTOR, F_GOAL_FACTOR, final_winner)

    # Print the winner of the final
    print('\nFinal summary:\n** ' + final_winner[0].name.upper() + ' ** have won the tournament!')

    # Update the list of tournament winners
    tournamentWinners.append([i + 1, final_winner[0].name])

    # Rank the teams by tournament performance (based on coefficients) and allocate prize money
    final_teams_ranking = []
    for t in teams:
        final_teams_ranking.append(t)
    final_teams_ranking = sorted(final_teams_ranking, key=lambda team: team.coefficient_season, reverse=True)
    prize_money = [45, 40, 36, 34, 28, 27, 26, 25, 19, 18, 17, 16, 15, 14, 13, 12]
    print('\nFinal tournament rankings:')
    # Print the header for the ranking table
    print('   Team' + ' '*(team_header_width - 3) + 'Score  ' + 'Prize ' + 'Bank')
    rank = 1
    for t in final_teams_ranking:
        t.prize_money_season = prize_money[rank - 1]
        t.bank += prize_money[rank - 1]
        print(str(rank) + ' '*(2 - len(str(rank))),
              t.name + ' '*(team_header_width - len(t.name)),
              str(t.coefficient_season) + ' '*(6-len(str(t.coefficient_season))),
              str(t.prize_money_season) + '   ', str(t.bank))
        rank += 1

    # Calculate change in team strengths based on available finances
    update_team_strength(final_teams_ranking)

    # Display the change in strength of each team for next season
    print('\nChanges in strength for next season:')
    update_squads(team_header_width, final_teams_ranking)

    # Reset the stats for next season and update starting values
    reset_season_stats(teams)

    print('')

# Display the all-time winners
print('All-time tournament winners:')
for w in tournamentWinners:
    print('Season ' + str(w[0]) + ':' + ' '*(len(str(number_seasons)) + 1 -len(str(w[0]))) + str(w[1]))

# Display the all-time stats
print('\nAll-time stats:')
stats_header = ' '*team_header_width + '| PL   | W    | D    | L    | GF   | GA   | GD   | PTS  | COEFF | PRIZE'
print(stats_header)
for t in final_teams_ranking:
    stats_row = t.name + str(' ')*(team_header_width-len(t.name)) \
                        + '| ' + str(t.played_forever) + str(' ')*(5-len(str(t.played_forever))) \
                        + '| ' + str(t.won_forever) + str(' ')*(5-len(str(t.won_forever)))\
                        + '| ' + str(t.drawn_forever) + str(' ')*(5-len(str(t.drawn_forever)))\
                        + '| ' + str(t.lost_forever) + str(' ')*(5-len(str(t.lost_forever))) \
                        + '| ' + str(t.goals_for_forever) + str(' ')*(5-len(str(t.goals_for_forever))) \
                        + '| ' + str(t.goals_against_forever) + str(' ')*(5-len(str(t.goals_against_forever))) \
                        + '| ' + str(t.goal_difference_forever) + str(' ')*(5-len(str(t.goal_difference_forever)))\
                        + '| ' + str(t.points_forever) + str(' ')*(5-len(str(t.points_forever))) \
                        + '| ' + str(int(t.coefficient_forever)) + str(' ')*(6-len(str(int(t.coefficient_forever))))\
                        + '| ' + str(t.prize_money_forever) + str(' ')*(4-len(str(t.prize_money_forever)))
    print(stats_row)
