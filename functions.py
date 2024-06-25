
from espn_api.football import League
# from espn_api.basketball import League
import json
import pandas as pd
import numpy as np
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash
import plotly.graph_objects as go
import json
import sqlite3
from num2words import num2words


# leagueId=78073200 #89402107
# teamId=5
# seasonId=2024#2024 #2023
# swid = '{7D53033F-1295-40F6-9303-3F129500F634}'#'{7D53033F-1295-40F6-9303-3F129500F634}'
# espn_s2 = 'AEBUQvJv3yhSogzUJVZeUPC6Hr%2FAktIAvjnOCDaxDzGNAkL%2Bo8aQyJ3jv68yMo7trr0dZswr6rxdtXOfMX%2Bc0MvZgNd1%2BACkkkS7FxL0mwgP7etnYM%2BmgYv2jDnEge5hySEQFDJq%2FnAWSEynmLSnW1gpO5FmYVljDY6zT26AFtU6za6gYqbtJ7JQFsSTRY0TTSdzQr30G%2FMrGq5bEbdf43E9W8wIt5p4dGbbMTw%2BhKsTkjgpINncMY%2FVqh2tkvRNnnE%3D'#'AEBHtlfL4hRIVkL9g2WOyX1JSb0oTv9EEhvIu%2B2zZF7Scsjh6idnV8EA5Yb0hu4HVRPG%2F51AKuK2eotrsAi06KkWb7lmi8UXCBX6X35MvI8H1VFM9Rmn6d4m8OaMOb63EbzebDUpj%2F5a9Nohj53vEjmPwNpbFcRtLmvFh52gi2W%2BIICrYBPN6%2FgOrM8qXloMbVrhHk%2F%2FY3n5yZPYPx8w9iDlRKQiAP2B%2Bi%2Bp2oMkp2Na754YaiJf5W6YwJZFD9VBTsc%3D'

# leagueId=89402107
# teamId=5
# seasonId=2022
# swid = '{7D53033F-1295-40F6-9303-3F129500F634}'
# espn_s2 = 'AEBHtlfL4hRIVkL9g2WOyX1JSb0oTv9EEhvIu%2B2zZF7Scsjh6idnV8EA5Yb0hu4HVRPG%2F51AKuK2eotrsAi06KkWb7lmi8UXCBX6X35MvI8H1VFM9Rmn6d4m8OaMOb63EbzebDUpj%2F5a9Nohj53vEjmPwNpbFcRtLmvFh52gi2W%2BIICrYBPN6%2FgOrM8qXloMbVrhHk%2F%2FY3n5yZPYPx8w9iDlRKQiAP2B%2Bi%2Bp2oMkp2Na754YaiJf5W6YwJZFD9VBTsc%3D'


def connect_db():
    db_name = "fantasyFootball.db"
    conn = sqlite3.connect(db_name)
    return conn

def connect():
    leagueId=89402107
    seasonId=2023
    swid = '{7D53033F-1295-40F6-9303-3F129500F634}'
    espn_s2 = 'AEBHtlfL4hRIVkL9g2WOyX1JSb0oTv9EEhvIu%2B2zZF7Scsjh6idnV8EA5Yb0hu4HVRPG%2F51AKuK2eotrsAi06KkWb7lmi8UXCBX6X35MvI8H1VFM9Rmn6d4m8OaMOb63EbzebDUpj%2F5a9Nohj53vEjmPwNpbFcRtLmvFh52gi2W%2BIICrYBPN6%2FgOrM8qXloMbVrhHk%2F%2FY3n5yZPYPx8w9iDlRKQiAP2B%2Bi%2Bp2oMkp2Na754YaiJf5W6YwJZFD9VBTsc%3D'

    league = League(league_id=leagueId, year=seasonId, espn_s2= espn_s2, swid=swid)
    return league

# league = League(league_id=leagueId, year=seasonId, espn_s2= espn_s2, swid=swid)
conn = connect_db()
league = connect()
num_teams = len(league.teams)
# print([team.team_name for team in league.teams])
# print(league.teams[2].roster)

def mode_function(x):
    return x.mode().iloc[0] if not x.mode().empty else pd.NA

def get_rosters():
    team_roster_dict = {}
    for i in range(0, num_teams):
        team_name = league.teams[i].team_name
        roster = []
        player_avg_points = []
        player_total_points = []
        player_elligible_slots = []
        for j in range(0, len(league.teams[i].roster)):
            roster.append(league.teams[i].roster[j].name)
            # player_avg_points.append(league.teams[i].roster[j].avg_points)
            # player_total_points.append(league.teams[i].roster[j].total_points)
            # player_elligible_slots.append(league.teams[i].roster[j].eligibleSlots)
        team_roster_dict[team_name] = roster
    # roster_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in team_roster_dict.items()]))#.transpose().reset_index(names='Teams')
    max_length = max(len(players) for players in team_roster_dict.values())
    # Create a DataFrame from the dictionary
    roster_df = pd.DataFrame({team: players + [None]*(max_length - len(players)) for team, players in team_roster_dict.items()})
    return roster_df

def proper_position(pos1, pos2):
    if pos1 != 'D/ST':
        position = min(pos1, pos2, key=len)
    else:
        position = pos1
    return position

def get_roster_stats(fantasy_name):
    for i in range(0, num_teams):
        team_name = league.teams[i].team_name
        if team_name == fantasy_name:
            roster = []
            player_avg_points = []
            player_total_points = []
            player_elligible_slots = []
            for j in range(0, len(league.teams[i].roster)):
                roster.append(league.teams[i].roster[j].name)
                player_avg_points.append(league.teams[i].roster[j].avg_points)
                player_total_points.append(league.teams[i].roster[j].total_points)
                player_elligible_slots.append(proper_position(league.teams[i].roster[j].eligibleSlots[0], league.teams[i].roster[j].eligibleSlots[1]))
            roster_stats_df = pd.DataFrame({'Roster':roster, 'Avg Points':player_avg_points, 'Total Points':player_total_points, 'Positions':player_elligible_slots})
    return roster_stats_df


def get_agg_roster_stats(fantasy_name):
    roster_stats_df = get_roster_stats(fantasy_name)
    agg_roster_stats = roster_stats_df.groupby(by='Positions', as_index=False).agg({'Avg Points':'mean', 'Total Points':'sum'}).round(3)
    return agg_roster_stats

# print(get_agg_roster_stats('Leeroy Jenkins'))

# print(team_roster_dict)
# print(json.dumps(team_roster_dict, indent=4))
def get_schedules():
    team_schedule_dict = {}
    for i in range(0, num_teams):
        team_name = league.teams[i].team_name
        schedule = []
        for j in range(0, len(league.teams[i].schedule)):
            # print(league.teams[i].schedule[j])
            try:
                schedule.append(league.teams[i].schedule[j].team_name)
            except:
                home_team = league.teams[i].schedule[j].home_team.team_name
                away_team = league.teams[i].schedule[j].away_team.team_name
                if home_team != team_name:
                    schedule.append(home_team)
                else:
                    schedule.append(away_team)

        team_schedule_dict[team_name] = schedule
    schedule_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in team_schedule_dict.items()]))
    return schedule_df
# print(len(get_schedules()))
def get_scores():
    team_scores_dict = {}
    for i in range(0, num_teams):
        team_name = league.teams[i].team_name
        scores_list = []
        for j in range(0, len(league.teams[i].scores)):
            scores_list.append(league.teams[i].scores[j])
            # print(team_name, scores_list)
        team_scores_dict[team_name] = scores_list
    scores_df = pd.DataFrame(team_scores_dict)
    return scores_df

# print(get_scores())

def get_stats(week: int=None):
    team_stats_dict = {}
    for i in range(0, num_teams):
        team_name = league.teams[i].team_name
        team_stats_dict[team_name] = {
            'Wins': league.teams[i].wins,
            'Losses': league.teams[i].losses,
            'Points For': round(league.teams[i].points_for,2),
            'Points Against': round(league.teams[i].points_against,2),
            'Acquisitions': league.teams[i].acquisitions,
            'Playoff Pct': league.teams[i].playoff_pct
        }
    # print(team_stats_dict)
    team_stats_df = pd.DataFrame(team_stats_dict).transpose().reset_index(names='Teams')
    power_df = get_power_rankings(week)
    team_stats_df = team_stats_df.merge(power_df, on='Teams')
    return team_stats_df

def get_opponent_scores():
    scores_df = get_scores()
    schedules_df = get_schedules()
    opponent_scores_dict = {}
    for i in range(0, num_teams):
        team = league.teams[i].team_name
        # print('team', team)
        opponents_scores_list = []
        for j in range(0, len(schedules_df[team])):
            opponent = schedules_df[team][j]
            # print('opponent', opponent)
            opponents_score = scores_df[opponent][j]
            opponents_scores_list.append(opponents_score)
            # print('opp_score', opponents_scores_list)
        opponent_scores_dict[team] = opponents_scores_list
        opponent_scores_df = pd.DataFrame(opponent_scores_dict)
    return opponent_scores_df

def get_power_rankings(week: int=None):
    power_dict = {float(k):v.team_name for (k,v) in league.power_rankings()}
    power_df = pd.DataFrame({'Power Ranking (espn)': power_dict.keys(), 'Teams': power_dict.values()})
    return power_df
# print(get_power_rankings())

def get_free_agents():
    position_inputs = ['QB', 'RB', 'WR', 'TE', 'D/ST', 'K', 'FLEX']
    free_agent_dict = {}
    for pos in position_inputs:
        free_agent_dict[pos] = {}
        for player in league.free_agents(size=5, position=pos):
            free_agent_dict[pos][player.name] = {'Avg Points': player.avg_points, 'Proj Points':player.projected_points, 'Opponent':player.pro_opponent}
    qb_free_agent_df = pd.DataFrame(free_agent_dict['QB']).transpose().reset_index(names='Free Agents').astype({'Avg Points': float, 'Proj Points': float})
    rb_free_agent_df = pd.DataFrame(free_agent_dict['RB']).transpose().reset_index(names='Free Agents').astype({'Avg Points': float, 'Proj Points': float})
    wr_free_agent_df = pd.DataFrame(free_agent_dict['WR']).transpose().reset_index(names='Free Agents').astype({'Avg Points': float, 'Proj Points': float})
    te_free_agent_df = pd.DataFrame(free_agent_dict['TE']).transpose().reset_index(names='Free Agents').astype({'Avg Points': float, 'Proj Points': float})
    dst_free_agent_df = pd.DataFrame(free_agent_dict['D/ST']).transpose().reset_index(names='Free Agents').astype({'Avg Points': float, 'Proj Points': float})
    k_free_agent_df = pd.DataFrame(free_agent_dict['K']).transpose().reset_index(names='Free Agents').astype({'Avg Points': float, 'Proj Points': float})
    flex_free_agent_df = pd.DataFrame(free_agent_dict['FLEX']).transpose().reset_index(names='Free Agents').astype({'Avg Points': float, 'Proj Points': float})

    qb_free_agent_df['Position'] = 'QB'
    rb_free_agent_df['Position'] = 'RB'
    wr_free_agent_df['Position'] = 'WR'
    te_free_agent_df['Position'] = 'TE'
    dst_free_agent_df['Position'] = 'D/ST'
    k_free_agent_df['Position'] = 'K'
    flex_free_agent_df['Position'] = 'FLEX'
        # if len(free_agent_dict) > 0:
        #     free_agent_dict = pd.concat
    all_free_agents_df = pd.concat([qb_free_agent_df, rb_free_agent_df, wr_free_agent_df, te_free_agent_df, dst_free_agent_df, k_free_agent_df, flex_free_agent_df], ignore_index=True)
    all_free_agents_df_stats = all_free_agents_df.groupby('Position', as_index=False).agg({'Avg Points':'mean', 'Proj Points':'mean'}).round(3)
    return all_free_agents_df, all_free_agents_df_stats


def reset_summary_table(week: int):
    # current_week = week
    # summary = pd.read_csv('summary_weekly.csv')
    # summary = summary.iloc[0:((current_week-1)*num_teams),:]
    # # if week == 1:
    # summary.to_csv('summary_sim.csv', index=False, header=True)
    # # else:
    # #     summary.to_csv('summary_sim.csv', index=False, header=False)
    # conn.execute(f'delete from summary_sim')
    summary_weekly = pd.read_sql(f'select * from summary_weekly where week <= {week}', conn)
    summary_weekly.to_sql('summary_sim', conn, index=False, if_exists='replace')
    return {'status': f'Summary table reset to week: {week}'}

def weekly_rankings_update(week: int):
    current_week = week
    reset_summary_table(week=current_week)


    players = [team.team_name for team in league.teams]

    schedules = get_schedules().to_dict('list')

    # if current_week == 1:
    #     init_ratings = {team.team_name:1400 for team in league.teams}
    #     with open('ratings.json', 'w') as file:
    #         json.dump(init_ratings, file, indent=4) 

    # with open('ratings.json', 'r') as file:
    #     ratings = json.load(file)
    # print(current_week)
    if current_week == 1:
        ratings = {team.team_name:1400 for team in league.teams}
    else:
        ratings = pd.read_sql_query(f'select player, rating from summary_weekly where week = {current_week-1}', conn)#.to_dict('records')
        # print(ratings)
        ratings = {item['player']:item['rating'] for item in ratings.to_dict('records')}
    # print(ratings)

    scores = {team.team_name:team.scores[current_week-1] for team in league.teams}


    scores_against_dict = get_opponent_scores().to_dict('list')
    scores_against = {team.team_name:scores_against_dict[team.team_name][current_week-1] for team in league.teams}


    outscore_league = {team.team_name:sum(scores[team.team_name] > x for x in scores.values()) for team in league.teams}


    results_weekly = {}
    for player in players:
        if scores[player] > scores[schedules[player][current_week-1]]:
            results_weekly[player] = 1
        elif scores[player] < scores[schedules[player][current_week-1]]:
            results_weekly[player] = 0
        elif scores[player] == scores[schedules[player][current_week-1]]:
            results_weekly[player] = 0.5


    new_rating = {}
    # print('\n')
    # print(ratings)
    for player in players:
        ratings_diff = ratings[schedules[player][current_week-1]] - ratings[player]
        expected_result = 1/(1+10**(ratings_diff/400))
        new_rating[player] = ratings[player] + 12*((results_weekly[player] - expected_result) + (outscore_league[player]-4.5))# + (outscore_league[player]-6)*1.5
    ratings = new_rating

    # with open('ratings.json', 'w') as file:
    #     json.dump(new_rating, file, indent=4) 


    summary = {}
    summary[current_week] = {}
    for player in players:
        summary[current_week][player] = {
            'rating': ratings[player],
            'score': scores[player],
            'score_against': scores_against[player],
            'weekly_result': results_weekly[player],
            'outscore_league': outscore_league[player],
            #'total_result': results_total[player],
            #'z_score': z_scores[player],
            #'total_score': total_scores[player]
            }


    # print(json.dumps(new_rating, indent=4))
    # print('\n\n')
    #print(json.dumps(summary, indent=4))

    sum_df = pd.DataFrame.from_dict({(i,j): summary[i][j] 
                            for i in summary.keys() 
                            for j in summary[i].keys()},
                        orient='index').reset_index()
    sum_df = sum_df.rename(columns={'level_0':'week', 'level_1':'player'})
    # print(sum_df)
    if current_week == 1:
        # sum_df.to_csv('summary_weekly.csv', index=False, header=True, mode='w')
        # sum_df.to_csv('summary_sim.csv', mode='a', index=False, header=True)

        sum_df.to_sql('summary_weekly', conn, index=False, if_exists='replace')
        sum_df.to_sql('summary_sim', conn, index=False, if_exists='append')
    else:
        # sum_df.to_csv('summary_weekly.csv', index=False, header=False, mode='a')
        # sum_df.to_csv('summary_sim.csv', mode='a', index=False, header=False)

        sum_df.to_sql('summary_weekly', conn, index=False, if_exists='append')
        sum_df.to_sql('summary_sim', conn, index=False, if_exists='append')
    # print(sum_df)
    
    return {'status':'weekly rankings updated'}




def season_simulation(current_week: int, sims: int):

    weekly_rankings_update(week=current_week)

    current_week = current_week+1
    season = 1
    numer_seasons = sims
    weeks_in_season = league.settings.reg_season_count
    rng_std = 50

    # players = ['ben', 'james', 'dan', 'hunter', 'tommy', 'chris', 'david', 'michael', 'ozzy', 'logan', 'josh', 'nelson']
    # league = connect()
    playoff_seeds = league.settings.playoff_team_count
    players = [team.team_name for team in league.teams]
    season_list = []
    week_list = []
    rating_list = []
    score_list = []
    scores_against_list = []
    results_list = []
    z_score_list = []
    outscore_league_list = []
    total_score_list = []


    schedules = get_schedules().to_dict('list')

    divisions = {team.team_name:team.division_name for team in league.teams}




    ### Begin simulation ################################################################################################
    #####################################################################################################################
    #####################################################################################################################
    while season <= numer_seasons:
        score_list_total = []
        total_results = []
        results_total = {}
        summary = {} 

        # with open('ratings.json', 'r') as file:
        #     ratings = json.load(file)
        
        ratings = pd.read_sql_query(f'select player, rating from summary_weekly where week = {current_week-1}', conn).to_dict("records")
        ratings = {item['player']:item['rating'] for item in ratings}

        scores_update = {team.team_name:sum(team.scores)/len(team.scores) for team in league.teams}

        for i in range(current_week, weeks_in_season+1):

            scores = {team.team_name:np.random.normal(scores_update[team.team_name], rng_std+(current_week-i),1)[0] for team in league.teams}

            mean = sum(scores.values())/len(scores.values())
            std = (sum([(x - mean)**2 for x in scores.values()])/len(scores.values()))**0.5

            z_scores = {team.team_name:(scores[team.team_name]-mean)/std for team in league.teams}
            
            outscore_league = {team.team_name:sum(scores[team.team_name] > x for x in scores.values()) for team in league.teams}

            # scores_against_dict = get_opponent_scores().to_dict('list')
            current_opp = {team.team_name:schedules[team.team_name][i-1] for team in league.teams}
            scores_against = {team.team_name:scores[current_opp[team.team_name]] for team in league.teams}
            # scores_against = {team.team_name:scores_against_dict[team.team_name][current_week-1] for team in league.teams}



            results_weekly = {}
            for player in players:
                if scores[player] > scores[schedules[player][i-1]]:
                    results_weekly[player] = 1
                elif scores[player] < scores[schedules[player][i-1]]:
                    results_weekly[player] = 0
                elif scores[player] == scores[schedules[player][i-1]]:
                    results_weekly[player] = 0.5
            
            
            # for player in players:
            #     total_results = []
            #     total_results.append(results_weekly[player])
            #     total_wins = sum(total_results)
            #     results_total[player] = total_wins

            week = {}
            summary[i] = {}
            for player in players:
                summary[i][player] = {
                    'rating': ratings[player],
                    'score': scores[player],
                    'score_against': scores_against[player],
                    'weekly_result': results_weekly[player],
                    'outscore_league': outscore_league[player]
                    #'total_result': results_total[player],
                    # 'z_score': z_scores[player],
                    #'total_score': total_scores[player]
                    }


            new_rating = {}
            # print('\n')
            # print(ratings)
            for player in players:
                ratings_diff = ratings[schedules[player][i-1]] - ratings[player]
                expected_result = 1/(1+10**(ratings_diff/400))
                new_rating[player] = ratings[player] + 12*((results_weekly[player] - expected_result) + (outscore_league[player]-4.5))

                #new_rating[player] = ratings[player] + 12*(results_weekly[player] - 1/(1+10**((ratings[player]-ratings[schedules[player][i-1]])/400))) + z_scores[player]*5
            ratings = new_rating
            # with open('ratings.json', 'w') as file:
            #     json.dump(new_rating, file, indent=4)
            # print(ratings)
            for player in players:
                rating_list.append(ratings[player])
                score_list.append(scores[player])
                scores_against_list.append(scores_against[player])
                results_list.append(results_weekly[player])
                z_score_list.append(z_scores[player])
                outscore_league_list.append(outscore_league[player])
                #total_score_list.append(total_scores[player])
                season_list.append(season)
                week_list.append(i)
            
            i += 1
        season += 1

    # with open('ratings.json', 'w') as file:
    #     json.dump(new_rating, file, indent=4)
    ### Analysis - Season Summary #######################################################################################
    #####################################################################################################################
    #####################################################################################################################


    weekly_summary = pd.DataFrame({'season':season_list, 'week': week_list, 'player':players*(weeks_in_season - (current_week-1))*numer_seasons, 'rating':rating_list, 'score':score_list, 'score_against':scores_against_list, 'weekly_result':results_list, 'outscore_league':outscore_league_list})


    season_summary = weekly_summary.groupby(['season', 'player']).agg({'rating': 'last', 'score': 'sum', 'score_against': 'sum', 'weekly_result': 'sum', 'outscore_league': 'sum'}).reset_index()

    divisions_list = []
    for player in season_summary['player']:
        divisions_list.append(divisions[player])

    season_summary['division'] = divisions_list

    season_summary.sort_values(by=['season', 'division', 'weekly_result', 'score'], ascending=False, inplace=True)
    season_summary['division_rank'] = 1
    season_summary['division_rank'] = season_summary.groupby(['season', 'division'])['division_rank'].cumsum()

    season_summary.sort_values(by=['season', 'weekly_result', 'score'], ascending=False, inplace=True)
    season_summary['overall_rank'] = 1
    season_summary['overall_rank'] = season_summary.groupby(['season'])['overall_rank'].cumsum()

    playoff_matrix_init = [1]*playoff_seeds + [0]*(len(players)-playoff_seeds)
    season_summary['playoffs'] = playoff_matrix_init*numer_seasons
    # print(season_summary.sort_values(by=['season','overall_rank'], ascending=True))
    # print(season_summary.dtypes)
    # print('\n\n')
    # print(season_summary)
    season_summary_agg = season_summary.groupby(['player']).agg({'rating': 'mean', 'score': 'mean', 'score_against': 'mean', 'weekly_result': 'mean', 'outscore_league': 'mean', 'division_rank': mode_function, 'overall_rank': mode_function, 'playoffs':'sum'}).reset_index().sort_values(by=['overall_rank'], ascending=False).round(3)
    # print(season_summary_agg.columns)
    season_summary_agg.columns = ['player', 'rating', 'score', 'score_against', 'result', 'outscore', 'division_rank', 'overall_rank', 'playoffs']
    # print(season_summary_agg)
    # print('\n\n')
    ### Analysis - Rank Counts

    seed_count = {}
    for seed in range(0,len(players)):
        seed_count[num2words(seed+1)] = {}
        for player in players:
            seed_count[num2words(seed+1)][player] = sum(season_summary[season_summary['player'] == player]['overall_rank'] == seed+1)
    # print(seed_count)

    seed_df = pd.DataFrame(seed_count).reset_index(names='Teams')
    # seed_df = seed_df.T
    # seed_df.index.name = 'Seed'
    # seed_df = seed_df.T
    # seed_df['Teams'] = seed_count[1].keys()
    # print(seed_df)
    


    # print('\n\n')

    ### Analysis - Weekly Summary #############################################################################################
    #####################################################################################################################
    #####################################################################################################################
    average_week = weekly_summary.groupby(['week', 'player']).agg({'rating': 'mean', 'score': 'mean', 'score_against': 'mean', 'weekly_result': 'median', 'outscore_league': 'median'}).reset_index()
    # print(average_week)
    # print(season_summary_agg)
    # if week == 0:
    #     average_week.to_csv('summary.csv', index=False, header=True, mode='w')   
    # else:
    if current_week > 1:
        # average_week.to_csv('summary_sim.csv', index=False, header=False, mode='a') 
        average_week.to_sql('summary_sim', conn, index=False, if_exists='append') 
    # season_summary_agg.to_csv('simulated_season_summary.csv')
    season_summary_agg.to_sql('simulated_season_summary', conn, index=False, if_exists='replace')
    # seed_df.to_csv('simulated_season_seed.csv')
    seed_df.to_sql('simulated_season_seed', conn, index=False, if_exists='replace')
    #print(json.dumps(summary, indent=4))


    # rest_of_season = pd.read_csv('summary.csv')
    # rest_of_season.columns = ['week', 'player', 'rating', 'score', 'score_against', 'wins', 'outscore_league']
    # rest_of_season_sum = rest_of_season.groupby(['player']).agg({'rating': 'last', 'score': 'sum', 'score_against': 'sum', 'wins': 'sum', 'outscore_league': 'sum'}).reset_index()

    # rest_of_season_sum = rest_of_season_sum.merge(season_summary_agg[['division_rank','overall_rank','playoffs']], on='player', how='left').sort_values(by=['playoffs'], ascending=False).reset_index(drop=True).round(3)

    # print(rest_of_season_sum)
    return {'status': 'season simulated'}
        # print(pos, league.free_agents(size=5, position=pos))
# print(get_free_agents())
# print(league.free_agents(size=5, position='QB')[0].projected_points)

# print(get_opponent_scores()['Leeroy Jenkins'].reset_index(name='Opponent_Scores').to_dict('records'))


def team_dash_layout(fantasy_name):
    # fantasy_name = 'Leeroy Jenkins'
    # print(str(fantasy_name))
    fantasy_names_no_space = {team.team_name.replace(' ',''):team.team_name for team in league.teams}
    fantasy_name = fantasy_names_no_space[fantasy_name]
    rosters_df = get_rosters()
    schedule_df = get_schedules()
    stats = get_stats()
    scores = get_scores()
    opponent_scores = get_opponent_scores()
    agg_roster_stats = get_agg_roster_stats(fantasy_name)
    free_agents = get_free_agents()
    # print(free_agents)

    logans_stats_df = stats.loc[stats['Teams'] == fantasy_name]

    logans_roster = rosters_df[fantasy_name].reset_index(name='Roster')#.merge(get_roster_stats(fantasy_name), on='Roster').iloc[:,1:].to_dict('records')
    logans_roster = logans_roster.merge(get_roster_stats(fantasy_name), on='Roster').iloc[:,1:].to_dict('records')

    logans_schedule = schedule_df[fantasy_name].reset_index(name='Schedule').to_dict('records')
    logans_schedule = [{'Schedule': item['Schedule']} for item in logans_schedule]

    logans_scores = scores[fantasy_name].reset_index(name='Scores').to_dict('records')
    logans_scores = [{'Scores': item['Scores']} for item in logans_scores] 

    logans_opponent_scores = opponent_scores[fantasy_name].reset_index(name='Opponent_Scores').to_dict('records')
    logans_opponent_scores = [{'Opponent Scores': item['Opponent_Scores']} for item in logans_opponent_scores]

    


    matchups = pd.concat([get_scores()[fantasy_name], get_opponent_scores()[fantasy_name]], axis=1)
    matchups.columns = ['Scores', 'Opponent_Scores']
    # print(matchups)

    weekly_stats = pd.read_sql(f'select week, player, round(rating/14,3) as [rating(logan)], score, score_against, outscore_league from summary_weekly where player like "{fantasy_name}%"', con=connect_db())
    # print(weekly_stats)
    # with open('ratings.json', 'r') as file:
    #         ratings = json.load(file)
    # current_ratings = pd.read_sql('select player, round(rating/14,3) as ratings from summary_weekly where week = (select max(week) from summary_weekly)')
    # current_ratings = pd.DataFrame({'Teams':ratings.keys(), 'Current Rating (logan)':ratings.values()}).round(3)
    current_ratings = weekly_stats.loc[weekly_stats['week'] == max(weekly_stats['week']), ['player','rating(logan)']]
    current_ratings.columns = ['Teams','Current Rating (logan)']
    # weekly_stats = pd.read_csv('summary_weekly.csv')
    current_league_wins = weekly_stats[['player','outscore_league']].groupby(by='player').agg({'outscore_league':'sum'}).reset_index()
    # current_league_wins = weekly_stats[['outscore_league']].sum()
    current_league_wins.columns = ['Teams', 'League Wins']
    stats = logans_stats_df.merge(current_ratings, on='Teams')#.sort_values(by=[''])
    stats = stats.merge(current_league_wins, on='Teams')#.sort_values(by=['League Wins','Current Rating','Points For'], ascending=False)
    # stats['Current Rating (logan)'] = round(stats['Current Rating (logan)']/14,3)

    weekly_stats_display = weekly_stats[['week','rating(logan)','score','score_against','outscore_league']]
    weekly_stats_display.columns = ['Week','Rating (logan)','Points For','Points Against','League Wins']

    # Create the double bar chart
    fig = go.Figure(data=[
        go.Bar(name='Scores', x=matchups.index, y=matchups['Scores']),
        go.Bar(name='Opponent Scores', x=matchups.index, y=matchups['Opponent_Scores'])
    ])
    fig.update_layout(barmode='group', xaxis_title='Week', yaxis_title='Scores')

    layout = [
        html.H1(fantasy_name),
        html.Div(className='row', children=[
            html.Div(className='twelve columns', children=[
                dash_table.DataTable(stats.to_dict('records'), page_size=20, style_table={'overflowX': 'auto', 'margin-left':'auto', 'margin-right':'auto'})
            ])
        ]),
        html.Br(),
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
                dash_table.DataTable(logans_roster, page_size=17, style_table={'overflowX': 'auto'}, sort_action='native')
            ]),
            html.Div(className='four columns', children=[
                html.Div(className='row', children='Team Stats', style={'textAlign': 'center', 'fontSize': 15}),
                dash_table.DataTable(agg_roster_stats.to_dict('records'), sort_action='native'),
                html.Br(),
                html.Div(className='row', children='Free Agent Stats', style={'textAlign': 'center', 'fontSize': 15}),
                dash_table.DataTable(free_agents[1].to_dict('records'), sort_action='native')
            ]),
            html.Div(className='four columns', children=[
                dash_table.DataTable(free_agents[0].to_dict('records'), page_size=17, style_table={'overflowY':'auto'}, sort_action='native')
            ])
        ]),
        html.Br(),
        html.Div(className='row', children=[
            html.Div(className='two columns', children=[
                dash_table.DataTable(logans_schedule, page_size=17, style_table={'overflowX': 'auto'})
            ]),
            # html.Div(className='two columns', children=[
            #     dash_table.DataTable(logans_scores, page_size=17, style_table={'overflowX': 'auto'})
            # ]),
            # html.Div(className='two columns', children=[
            #     dash_table.DataTable(logans_opponent_scores, page_size=17, style_table={'overflowX': 'auto'})
            # ]),
            html.Div(className='eight columns', children=[
                dash_table.DataTable(weekly_stats_display.to_dict('records'), page_size=17, style_table={'overflowX': 'auto'})
            ])
        ]),
        html.Div(className='row', children=[
            # dcc.Graph(figure=px.bar(logans_scores, title='Points Scored per Week'))
            dcc.Graph(figure=fig)
        ])
    ]
    return layout

# def stats_dash_layout():
#     rest_of_season = pd.read_csv('summary_sim.csv')
#     rest_of_season.columns = ['week', 'player', 'rating', 'score', 'score_against', 'wins', 'outscore_league']
#     rest_of_season_sum = rest_of_season.groupby(['player']).agg({'rating': 'last', 'score': 'sum', 'score_against': 'sum', 'wins': 'sum', 'outscore_league': 'sum'}).reset_index().round(3)
#     # print(rest_of_season_sum[['player','score']])
#     season_summary = pd.read_csv('simulated_season_summary.csv')
#     rest_of_season_sum = rest_of_season_sum.merge(season_summary[['player','division_rank','overall_rank','playoffs']], on='player', how='left').sort_values(by=['playoffs', 'overall_rank', 'rating'], ascending=False).reset_index(drop=True).round(3)
#     rest_of_season_sum.columns = ['Teams', 'Proj Rating (logan)', 'Proj PF', 'Proj PA', 'Proj Wins', 'Proj League Wins', 'Proj Seed (div)', 'Proj Seed (overall)', 'Playoff %']
#     rest_of_season_sum['Playoff %'] = rest_of_season_sum['Playoff %'] / 100
#     # rest_of_season_sum = rest_of_season_sum.merge(season_summary_agg[['division_rank','overall_rank','playoffs']], on='player', how='left').sort_values(by=['playoffs'], ascending=False).reset_index(drop=True).round(3)
#     # rest_of_season_sum['Proj Rating'] = round(rest_of_season_sum['Proj Rating'] / 1400,3)

#     stats = get_stats()

#     with open('ratings.json', 'r') as file:
#             ratings = json.load(file)
#     current_ratings = pd.DataFrame({'Teams':ratings.keys(), 'Current Rating (logan)':ratings.values()}).round(3)
#     weekly_stats = pd.read_csv('summary_weekly.csv')
#     current_league_wins = weekly_stats[['player','outscore_league']].groupby(by='player').agg({'outscore_league':'sum'}).reset_index()
#     current_league_wins.columns = ['Teams', 'League Wins']
#     stats = stats.merge(current_ratings, on='Teams')#.sort_values(by=[''])
#     stats = stats.merge(current_league_wins, on='Teams').sort_values(by=['League Wins','Current Rating (logan)','Points For'], ascending=False)
#     # stats['Current Rating'] = round(stats['Current Rating'] / 1400, 3)


#     layout = [
#         html.Div(className='row', children='Stats', style={'textAlign': 'center', 'fontSize': 30}),
#         html.Div(className='row', children=[
#             html.Div(className='centered-table', children=[
#                 dash_table.DataTable(data=stats.to_dict('records'), style_table={'overflowX': 'auto', 'margin-left':'auto', 'margin-right':'auto'}, sort_action='native')
#                 ])
#         ]),
#         # html.Div(className='four columns', children=[
#         #         dcc.RadioItems(options=['Wins','Losses','Points For','Points Against','Acquisitions','Playoff Pct', 'Power Ranking'], value='Points For', id='stats-radio-item')
#         # ]),
#         # html.Div(className='row', children=[
#         #     html.Div(className='eight columns', children=[
#         #         dcc.Graph(figure={}, id='stats-graph')
#         #     ])
#         # ]),
#         html.Br(),
#         html.Div(className='row', children='Projected Stats', style={'textAlign': 'center', 'fontSize': 30}),
#         html.Div(className='row', children=[
#             html.Div(className='centered-table', children=[
#                 dash_table.DataTable(rest_of_season_sum.to_dict('records'), sort_action='native')
#             ]),
#             html.Div(className='row', children=[
#                 html.Div(className='two columns', children=[
#                     dcc.RadioItems(options=['Proj Rating (logan)', 'Proj PF', 'Proj PA', 'Proj Wins', 'Proj League Wins', 'Proj Seed (div)', 'Proj Seed (overall)', 'Playoff %'], value='Proj Rating (logan)', id='adv-stats-radio-item')
#                 ]),
#                 html.Div(className='eight columns', children=[
#                     dcc.Graph(figure={}, id='adv-stats-graph')
#                 ])
#             ])
#         ])
#     ]

#     return layout

# print([1]*6 + [0]*4)
# season_simulation(week=0)