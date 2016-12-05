#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).

Database models part - defines table for storing scraped data.
Direct run will create the table.
"""

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from .settings import DATABASE


DeclarativeBase = declarative_base()


def db_connect():
    """Performs database connection using database settings from settings.py.

    Returns sqlalchemy engine instance.

    """
    return create_engine(URL(**DATABASE))


def create_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Players(DeclarativeBase):
    __tablename__ = "players"

    player_id = Column('player_id', Integer, primary_key=True)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    birthdate = Column('birthdate', Date)
    school = Column('school', String)    
    country = Column('country', String)  
    last_affiliation = Column('last_affiliation', String)
    height = Column('height', String) 
    weight = Column('weight', String) 
    season_exp = Column('season_exp', String) 
    jersey = Column('jersey', String) 
    position = Column('position', String)      
    dleague_flag = Column('dleague_flag', String)
    draft_year = Column('draft_year', String)   
    draft_round = Column('draft_round', String)   
    draft_number = Column('draft_number', String)           
    roster_status = Column('roster_status', String)
    from_year = Column('from_year', String)
    to_year = Column('to_year', String)
    team_id = Column('team_id', String)


class Teams(DeclarativeBase):
    __tablename__ = "teams"

    team_id = Column('team_id', Integer, primary_key=True)
    abbreviation = Column('abbreviation', String)
    name = Column('name', String)
  
class Shots(DeclarativeBase):
    __tablename__ = "shots"

    game_id = Column('game_id', Integer, primary_key=True)
    game_event_id = Column('game_event_id', Integer, primary_key=True)
    player_id = Column('player_id', Integer)
    loc_x = Column('loc_x', Integer)
    loc_y = Column('loc_y', Integer)
    shot_made_flag = Column('shot_made_flag', Integer)
    shot_attempted_flag = Column('shot_attempted_flag', Integer)

class Games(DeclarativeBase):
    __tablename__ = "games"

    game_id = Column('game_id', Integer, primary_key=True)
    game_date = Column('game_date', Date)
    periods = Column('periods', Integer)
    home_team_id = Column('home_team_id ', Integer)
    visitor_team_id = Column('visitor_team_id', Integer)

class PlayerGameStats(DeclarativeBase):
    __tablename__ = "player_game_stats"

    game_id = Column('game_id', Integer, primary_key=True)
    player_id = Column('player_id', Integer, primary_key=True)
    ft_pct = Column('ft_pct',Float)
    fg3a = Column('fg3a', Integer)
    ast = Column('ast', Integer)
    plus_minus = Column('plus_minus', Integer)
    minutes = Column('minutes', String)
    pts = Column('pts', Integer)
    fg_pct = Column('fg_pct',Float)
    fg3m = Column('fg3m', Integer)
    oreb = Column('oreb', Integer)
    fta = Column('fta', Integer)
    to = Column('to', Integer)
    fg3_pct = Column('fg3_pct', Float)
    pf = Column('pf', Integer)
    fgm = Column('fgm', Integer)
    blk = Column('blk', Integer)
    stl = Column('stl', Integer)
    reb = Column('reb', Integer)
    dreb = Column('dreb', Integer)
    ftm = Column('ftm', Integer)
    fga = Column('fga', Integer)

class TeamGameStats(DeclarativeBase):
    __tablename__ = "team_game_stats"    

    game_id = Column('game_id', Integer, primary_key=True)
    team_id = Column('team_id', Integer, primary_key=True)
    ft_pct = Column('ft_pct',Float)
    fg3a = Column('fg3a', Integer)
    ast = Column('ast', Integer)
    plus_minus = Column('plus_minus', Integer)
    minutes = Column('minutes', String)
    pts = Column('pts', Integer)
    fg_pct = Column('fg_pct',Float)
    fg3m = Column('fg3m', Integer)
    oreb = Column('oreb', Integer)
    fta = Column('fta', Integer)
    to = Column('to', Integer)
    fg3_pct = Column('fg3_pct', Float)
    pf = Column('pf', Integer)
    fgm = Column('fgm', Integer)
    blk = Column('blk', Integer)
    stl = Column('stl', Integer)
    reb = Column('reb', Integer)
    dreb = Column('dreb', Integer)
    ftm = Column('ftm', Integer)
    fga = Column('fga', Integer)  

class GameRosters(DeclarativeBase):
    __tablename__ = "game_rosters"
    game_id = Column('game_id', Integer, primary_key=True)
    team_id = Column('team_id', Integer, primary_key=True)
    player_id = Column('player_id', Integer, primary_key=True)   
    
class EventPlayersTable(DeclarativeBase):
    __tablename__ = "event_players"     

    game_id = Column('game_id', Integer, primary_key=True)
    game_event_id = Column('game_event_id', Integer, primary_key=True) 
    matchup_id = Column('matchup_id', Integer) 

class Matchups(DeclarativeBase):
    __tablename__ = "matchups"

    game_id = Column('game_id', Integer, primary_key=True)
    matchup_id = Column('matchup_id', Integer, primary_key=True) 
    home_player1_id = Column('home_player1_id', Integer) 
    home_player2_id = Column('home_player2_id', Integer) 
    home_player3_id = Column('home_player3_id', Integer) 
    home_player4_id = Column('home_player4_id', Integer) 
    home_player5_id = Column('home_player5_id', Integer) 
    away_player1_id = Column('away_player1_id', Integer) 
    away_player2_id = Column('away_player2_id', Integer) 
    away_player3_id = Column('away_player3_id', Integer) 
    away_player4_id = Column('away_player4_id', Integer) 
    away_player5_id = Column('away_player5_id', Integer) 



