from flask import render_template, request, redirect, flash,url_for
from models import  Games, Teams, Players, PlayerGameStats, TeamGameStats, GameRosters, Shots, Matchups, db #Category, Todo, Priority,
from todoapp import app
from datetime import date
import datetime
import json

def unique_dicts(l):
    seen = set()
    new_l = []
    for d in l:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)

    return new_l

@app.route('/')
def list_home(game_date = date(year=2008,month=10,day=31) ):

   
    # dt = game_date = date(day=int(day), month=int(month), year=int(year))
    return render_template(
        'list.html',
        games = Games.query.filter_by(game_date=game_date).all(),
        teams = Teams.query.all(),
        date = game_date.strftime('%A, %B %d, %Y'),
        all_games =  Games.query.with_entities(Games.game_date).group_by(Games.game_date).order_by(Games.game_date).all()[:20],
        curr_date = game_date
        # todos=Todo.query.all(),#join(Priority).order_by(Priority.value.desc())
    )


@app.route('/<game_date>')
def list_all(game_date = "2008-31-10"):

    year, month, day= str(game_date).split("-")
    dt = game_date = date(day=int(day), month=int(month), year=int(year))
    return render_template(
        'list.html',
        games = Games.query.filter_by(game_date=dt).all(),
        teams = Teams.query.all(),
        date = game_date.strftime('%A, %B %d, %Y'),
        all_games =  Games.query.with_entities(Games.game_date).group_by(Games.game_date).order_by(Games.game_date).all()[:20],
        curr_date = game_date
        # todos=Todo.query.all(),#join(Priority).order_by(Priority.value.desc())
    )

@app.route('/game/<int:game_id>')
def view_game(game_id):
    rosters = GameRosters.query.filter_by(game_id=game_id).all()
    game = Games.query.get(game_id)
    player_stats = PlayerGameStats.query.filter_by(game_id=game_id).join(Players).all()
    team_stats = TeamGameStats.query.filter_by(game_id=game_id).all()
    return render_template(
        'game.html',
        game = game,
        team_stats = team_stats,
        rosters = rosters
    )


@app.route('/game/<int:game_id>/shots/<int:team_id>/<int:player_id>/<int:matchup_id>')
def view_game_shots(game_id, team_id, player_id,matchup_id):
    team_stats = TeamGameStats.query.filter_by(game_id=game_id).all()
    shots =Shots.query.filter_by(game_id=game_id).all()
    roster = GameRosters.query.filter_by(game_id=game_id).all()
    game = Games.query.get(game_id)
    roster_dict = {}
    curr_team_roster = []
    
    if player_id == 0:
        off_team = team_id
    else:
        for player in roster:
            if player.player_id == player_id:
                off_team = player.team_id
                if player.team_id == game.home_team_id:
                    def_team = game.visitor_team_id
                else:
                    def_team = game.home_team_id


    for player in roster:
        roster_dict[player.player_id] = player.team_id
        if player.team_id == team_id: 
            curr_team_roster.append(player)


    matchups = Matchups.query.filter_by(game_id=game_id).all()

    home_matchups = [] 
    away_matchups = []
    home_matchup_map = {}
    curr_home_match = 1
    home_seen = []
    away_matchup_map = {}
    curr_away_match = 1
    away_seen = []
    for matchup in matchups:  
        h_d = {}  
        h_d[1] =  matchup.home_player1_id
        h_d[2] =  matchup.home_player2_id
        h_d[3] =  matchup.home_player3_id
        h_d[4] =  matchup.home_player4_id
        h_d[5] =  matchup.home_player5_id
        h_d['1_name'] =  matchup.home_1.first_name[0] + ". " + matchup.home_1.last_name
        h_d['2_name'] =  matchup.home_2.first_name[0] + ". " + matchup.home_2.last_name
        h_d['3_name'] =  matchup.home_3.first_name[0] + ". " + matchup.home_3.last_name
        h_d['4_name'] =  matchup.home_4.first_name[0] + ". " + matchup.home_4.last_name
        h_d['5_name'] =  matchup.home_5.first_name[0] + ". " + matchup.home_5.last_name
        home_matchups.append(h_d)

        home_list = [h_d[1],h_d[2],h_d[3],h_d[4],h_d[5]]
        if home_list not in home_seen:
            home_seen.append(home_list)
            home_matchup_map[matchup.matchup_id] = curr_home_match
            curr_home_match += 1
        else:
            home_matchup_map[matchup.matchup_id] = home_seen.index(home_list)

        a_d = {}  
        a_d[1] =  matchup.away_player1_id
        a_d[2] =  matchup.away_player2_id
        a_d[3] =  matchup.away_player3_id
        a_d[4] =  matchup.away_player4_id
        a_d[5] =  matchup.away_player5_id
        a_d['1_name'] =  matchup.away_1.first_name[0] + ". " + matchup.away_1.last_name
        a_d['2_name'] =  matchup.away_2.first_name[0] + ". " + matchup.away_2.last_name
        a_d['3_name'] =  matchup.away_3.first_name[0] + ". " + matchup.away_3.last_name
        a_d['4_name'] =  matchup.away_4.first_name[0] + ". " + matchup.away_4.last_name
        a_d['5_name'] =  matchup.away_5.first_name[0] + ". " + matchup.away_5.last_name
        away_matchups.append(a_d)

        away_list = [a_d[1],a_d[2],a_d[3],a_d[4],a_d[5]]
        if away_list not in away_seen:
            away_seen.append(away_list)
            away_matchup_map[matchup.matchup_id] = curr_away_match
            curr_away_match += 1
        else:
            away_matchup_map[matchup.matchup_id] = away_seen.index(away_list)
    
    home_matchups = unique_dicts(home_matchups)
    away_matchups = unique_dicts(away_matchups)

    for i, matchup in enumerate(home_matchups): 
        matchup['id'] = i + 1
    for i, matchup in enumerate(away_matchups): 
        matchup['id'] = i + 1


    if int(game.home_team_id) == int(team_id):
        with open("test.txt","a") as fo:
        offensive_matchup_map = home_matchup_map
        offensive_matchups = home_matchups
        defensive_matchups = away_matchups
    else:
        with open("test.txt","a") as fo:
            offensive_matchup_map = away_matchup_map
            offensive_matchups = away_matchups
            defensive_matchups = home_matchups

    shot_list = []
    if player_id == 0:
        for shot in shots:
            if roster_dict[shot.player_id] == team_id:
                shot_dict = {}
                shot_dict['x'] = shot.loc_x
                shot_dict['y'] = shot.loc_y
                shot_dict['game_id'] = shot.game_id
                shot_dict['game_event_id'] = shot.game_event_id
                shot_dict['player_id'] = shot.player_id
                shot_dict['shot_made_flag'] = shot.shot_made_flag
                shot_list.append(shot_dict)
    else:
        for shot in shots:
            if roster_dict[shot.player_id] == team_id and shot.player_id == player_id:
                if matchup_id == 0 or matchup_id == offensive_matchup_map[shot.matchup.matchup_id]:
                    shot_dict = {}
                    shot_dict['x'] = shot.loc_x
                    shot_dict['y'] = shot.loc_y
                    shot_dict['game_id'] = shot.game_id
                    shot_dict['game_event_id'] = shot.game_event_id
                    shot_dict['player_id'] = shot.player_id
                    shot_dict['shot_made_flag'] = shot.shot_made_flag
                    shot_list.append(shot_dict)        

    # only send matchups that the player was in for
    off_cop = offensive_matchups[:]
    offensive_matchups = []
    for match in off_cop:
        if player_id in match.values():
            offensive_matchups.append(match)
    

    return render_template(
        'shots.html',
        shots = json.dumps(shot_list),
        game = game,
        team_stats = team_stats,
        rosters = roster,
        curr_team = team_id,
        curr_player = player_id,
        curr_matchup = matchup_id,
        curr_team_roster = curr_team_roster,
        off_matchups = offensive_matchups,
        def_matchups = defensive_matchups
    )    



