from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy #, hybrid_property
# from flask.ext.sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.hybrid import hybrid_property
from todoapp import app

db = SQLAlchemy(app)

class Players(db.Model):
    __tablename__ = "players"

    player_id = db.Column('player_id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String)
    last_name = db.Column('last_name', db.String)
    birthdate = db.Column('birthdate', db.Date)
    school = db.Column('school', db.String)    
    country = db.Column('country', db.String)  
    last_affiliation = db.Column('last_affiliation', db.String)
    height = db.Column('height', db.String) 
    weight = db.Column('weight', db.String) 
    season_exp = db.Column('season_exp', db.String) 
    jersey = db.Column('jersey', db.String) 
    position = db.Column('position', db.String)      
    dleague_flag = db.Column('dleague_flag', db.String)
    draft_year = db.Column('draft_year', db.String)   
    draft_round = db.Column('draft_round', db.String)   
    draft_number = db.Column('draft_number', db.String)           
    roster_status = db.Column('roster_status', db.String)
    from_year = db.Column('from_year', db.String)
    to_year = db.Column('to_year', db.String)
    team_id = db.Column('team_id', db.String)

class EventPlayersTable(db.Model):
    __tablename__ = "event_players"     

    game_id = db.Column('game_id', db.Integer, primary_key=True)
    game_event_id = db.Column('game_event_id', db.Integer, primary_key=True) 
    matchup_id = db.Column('matchup_id', db.Integer) 

class Teams(db.Model):
    __tablename__ = "teams"

    team_id = db.Column('team_id', db.Integer, primary_key=True)
    abbreviation = db.Column('abbreviation', db.String)
    name = db.Column('name', db.String)
  
class Shots(db.Model):
    __tablename__ = "shots"

    game_id = db.Column('game_id', db.Integer, primary_key=True)
    game_event_id = db.Column('game_event_id', db.Integer, primary_key=True)
    player_id = db.Column('player_id', db.Integer)
    loc_x = db.Column('loc_x', db.Integer)
    loc_y = db.Column('loc_y', db.Integer)
    shot_made_flag = db.Column('shot_made_flag', db.Integer)
    shot_attempted_flag = db.Column('shot_attempted_flag', db.Integer)

    matchup = db.relationship('EventPlayersTable')

    __table_args__ = (
        db.ForeignKeyConstraint(
            [game_event_id, game_id],
            [EventPlayersTable.game_event_id, EventPlayersTable.game_id]
    ),) 



    # team_id = db.relationship('GameRosters')


class Games(db.Model):
    __tablename__ = "games"

    game_id = db.Column('game_id', db.Integer, primary_key=True)
    game_date = db.Column('game_date', db.Date)
    periods = db.Column('periods', db.Integer)
    home_team_id = db.Column('home_team_id ', db.Integer, db.ForeignKey(Teams.team_id))
    visitor_team_id = db.Column('visitor_team_id', db.Integer,db.ForeignKey(Teams.team_id))

    home_team = db.relationship('Teams', foreign_keys='[Games.home_team_id]')
    visitor_team = db.relationship('Teams', foreign_keys='[Games.visitor_team_id]')



class PlayerGameStats(db.Model):
    __tablename__ = "player_game_stats"

    game_id = db.Column('game_id', db.Integer, primary_key=True)
    player_id = db.Column('player_id', db.Integer, db.ForeignKey(Players.player_id), primary_key=True)
    ft_pct = db.Column('ft_pct',db.Float)
    fg3a = db.Column('fg3a', db.Integer)
    ast = db.Column('ast', db.Integer)
    plus_minus = db.Column('plus_minus', db.Integer)
    minutes = db.Column('minutes', db.String)
    pts = db.Column('pts', db.Integer)
    fg_pct = db.Column('fg_pct',db.Float)
    fg3m = db.Column('fg3m', db.Integer)
    oreb = db.Column('oreb', db.Integer)
    fta = db.Column('fta', db.Integer)
    to = db.Column('to', db.Integer)
    fg3_pct = db.Column('fg3_pct', db.Float)
    pf = db.Column('pf', db.Integer)
    fgm = db.Column('fgm', db.Integer)
    blk = db.Column('blk', db.Integer)
    stl = db.Column('stl', db.Integer)
    reb = db.Column('reb', db.Integer)
    dreb = db.Column('dreb', db.Integer)
    ftm = db.Column('ftm', db.Integer)
    fga = db.Column('fga', db.Integer)
    
    @hybrid_property
    def seconds(self):
        if self.minutes is None:
            return 0
        else:
            mins, secs = self.minutes.split(":")
            return int(mins) * 60 + int(secs)

        return self.minutes

    player_info = db.relationship('Players', foreign_keys='[PlayerGameStats.player_id]')

class TeamGameStats(db.Model):
    __tablename__ = "team_game_stats"    

    game_id = db.Column('game_id', db.Integer, primary_key=True)
    team_id = db.Column('team_id', db.Integer, primary_key=True)
    ft_pct = db.Column('ft_pct',db.Float)
    fg3a = db.Column('fg3a', db.Integer)
    ast = db.Column('ast', db.Integer)
    plus_minus = db.Column('plus_minus', db.Integer)
    minutes = db.Column('minutes', db.String)
    pts = db.Column('pts', db.Integer)
    fg_pct = db.Column('fg_pct',db.Float)
    fg3m = db.Column('fg3m', db.Integer)
    oreb = db.Column('oreb', db.Integer)
    fta = db.Column('fta', db.Integer)
    to = db.Column('to', db.Integer)
    fg3_pct = db.Column('fg3_pct', db.Float)
    pf = db.Column('pf', db.Integer)
    fgm = db.Column('fgm', db.Integer)
    blk = db.Column('blk', db.Integer)
    stl = db.Column('stl', db.Integer)
    reb = db.Column('reb', db.Integer)
    dreb = db.Column('dreb', db.Integer)
    ftm = db.Column('ftm', db.Integer)
    fga = db.Column('fga', db.Integer)  

class GameRosters(db.Model):
    __tablename__ = "game_rosters"
    game_id = db.Column('game_id', db.Integer, primary_key=True)
    player_id = db.Column('player_id', db.Integer, primary_key=True) 
    team_id = db.Column('team_id', db.Integer)

    player_stats = db.relationship('PlayerGameStats')

    __table_args__ = (
        db.ForeignKeyConstraint(
            [player_id, game_id],
            [PlayerGameStats.player_id, PlayerGameStats.game_id]
    ),)    



class Matchups(db.Model):
    __tablename__ = "matchups"

    game_id = db.Column('game_id', db.Integer, primary_key=True)
    matchup_id = db.Column('matchup_id', db.Integer, primary_key=True) 
    home_player1_id = db.Column('home_player1_id', db.Integer, db.ForeignKey(Players.player_id)) 
    home_player2_id = db.Column('home_player2_id', db.Integer, db.ForeignKey(Players.player_id)) 
    home_player3_id = db.Column('home_player3_id', db.Integer, db.ForeignKey(Players.player_id)) 
    home_player4_id = db.Column('home_player4_id', db.Integer, db.ForeignKey(Players.player_id)) 
    home_player5_id = db.Column('home_player5_id', db.Integer, db.ForeignKey(Players.player_id)) 
    away_player1_id = db.Column('away_player1_id', db.Integer, db.ForeignKey(Players.player_id)) 
    away_player2_id = db.Column('away_player2_id', db.Integer, db.ForeignKey(Players.player_id)) 
    away_player3_id = db.Column('away_player3_id', db.Integer, db.ForeignKey(Players.player_id)) 
    away_player4_id = db.Column('away_player4_id', db.Integer, db.ForeignKey(Players.player_id)) 
    away_player5_id = db.Column('away_player5_id', db.Integer, db.ForeignKey(Players.player_id)) 

    home_1 = db.relationship('Players', foreign_keys='[Matchups.home_player1_id]')
    home_2 = db.relationship('Players', foreign_keys='[Matchups.home_player2_id]')
    home_3 = db.relationship('Players', foreign_keys='[Matchups.home_player3_id]')
    home_4 = db.relationship('Players', foreign_keys='[Matchups.home_player4_id]')
    home_5 = db.relationship('Players', foreign_keys='[Matchups.home_player5_id]')
    away_1 = db.relationship('Players', foreign_keys='[Matchups.away_player1_id]')
    away_2 = db.relationship('Players', foreign_keys='[Matchups.away_player2_id]')
    away_3 = db.relationship('Players', foreign_keys='[Matchups.away_player3_id]')
    away_4 = db.relationship('Players', foreign_keys='[Matchups.away_player4_id]')
    away_5 = db.relationship('Players', foreign_keys='[Matchups.away_player5_id]')


