#! python3
# This file defines a common content and style format for each group table

# Define the group table header
table_header = '        | STR  | PL  | W   | D   | L   | GF  | GA  | GD  | PTS'


# Define group table content
def groups_table(sort_groups, team_header_width):
    for g in sort_groups:
        print('\n' + str.upper(g[1]) + ' ' + table_header)
        for t in g[0]:
            league_row = t.name + str(' ')*(team_header_width-len(t.name)) \
                        + '| ' + str(t.strength1) + str(' ')*(5-len(str(t.strength1))) \
                        + '| ' + str(t.played_season) + str(' ')*(4-len(str(t.played_season)))\
                        + '| ' + str(t.won_season) + str(' ')*(4-len(str(t.won_season))) \
                        + '| ' + str(t.drawn_season) + str(' ')*(4-len(str(t.drawn_season))) \
                        + '| ' + str(t.lost_season) + str(' ')*(4-len(str(t.lost_season))) \
                        + '| ' + str(t.goals_for_season) + str(' ')*(4-len(str(t.goals_for_season)))\
                        + '| ' + str(t.goals_against_season) + str(' ')*(4-len(str(t.goals_against_season))) \
                        + '| ' + str(t.goal_difference_season) + str(' ')*(4-len(str(t.goal_difference_season)))\
                        + '| ' + str(t.points_season) + str(' ')*(4-len(str(t.points_season)))
            print(league_row)
    return


# Sort groups by points, then any tie-breaker criteria
def sort_groups(group_a, group_b, group_c, group_d):
    table_sort = lambda team: (team.points_season, (team.goal_difference_season, (-team.strength1, team.name)))
    sort_group_a = sorted(group_a, key=table_sort, reverse=True)
    sort_group_b = sorted(group_b, key=table_sort, reverse=True)
    sort_group_c = sorted(group_c, key=table_sort, reverse=True)
    sort_group_d = sorted(group_d, key=table_sort, reverse=True)
    sorted_groups = [[sort_group_a, 'Group A'], [sort_group_b, 'Group B'],
                     [sort_group_c, 'Group C'], [sort_group_d, 'Group D']]
    return sorted_groups
