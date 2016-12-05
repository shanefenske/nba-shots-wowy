#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).

Scrapy pipeline part - stores scraped items in the database.
"""
import sys
from sqlalchemy.orm import sessionmaker
from .models import Players, Teams, Shots, Games, PlayerGameStats, TeamGameStats, GameRosters, EventPlayersTable, Matchups, db_connect, create_table
from nba_app.items import Game, PlayerGameStat, TeamGameStat, GameRoster, EventPlayers, Matchup

class PlayerPipeline(object):
    """Pipeline for storing every NBA player's id in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.

        Creates all tables if they do not exist.

        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Save ids in the database.

        """
        session = self.Session()
        player = Players(**item)

        try:
            session.add(player)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

class TeamPipeline(object):
    """Pipeline for storing every NBA team's id in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.

        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Save ids in the database.

        """
        session = self.Session()
        team = Teams(**item)

        try:
            session.add(team)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

class ShotPipeline(object):   
    """Pipeline for storing every NBA player's id in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Save ids in the database.

        """
        session = self.Session()
        shot = Shots(**item)

        try:
            session.add(shot)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item 


class GamesPipeline(object):   
    """Pipeline for storing everything that is stored in the parsed PBP files"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.

        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Save ids in the database.

        """
        session = self.Session()
        
        item_to_add = None 

        if isinstance(item, Game):
            item_to_add = Games(**item)         
        elif isinstance(item, PlayerGameStat):
            item_to_add = PlayerGameStats(**item)
        elif isinstance(item, TeamGameStat):
            item_to_add = TeamGameStats(**item)
        elif isinstance(item, GameRoster):
            item_to_add = GameRosters(**item)   
        elif isinstance(item, EventPlayers):
            item_to_add = EventPlayersTable(**item) 
        elif isinstance(item, Matchup):
            item_to_add = Matchups(**item)                                            

        # print("\n\n\n\n\ADDING ITEM\n\n\n\n\n\n\n\n\n\n\n\n\n")
        try:
            session.add(item_to_add)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()   

        return item 