#! -*- coding: utf-8 -*-

"""

"""
from scrapy import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from nba_app.items import Game, PlayerGameStat, TeamGameStat, GameRoster, EventPlayers, Matchup
import json
import os
from ..settings import DATABASE
from ..tools import string_height_to_inches
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text

class ParsedPBPSpider(BaseSpider):
    """
    Crawl parsed pbp files to yield Games, PlayerGameStats, TeamGameStats, 
    Plays, GameRosters, EventPlayers and also make API request to get game_date
    """
    name = "pbp"

    custom_settings = {
        'ITEM_PIPELINES': {
            'nba_app.pipelines.GamesPipeline': 300,
        }
    }

    def start_requests(self):
        """
        Override start_requests because we want dynamic start_url generation
        """
        # load pbp from ../../pbp
        pbp_dir = "/Users/shanefenske/Desktop/nba-scrape/pbp"
        
        years_dirs = next(os.walk(pbp_dir))[1]
        for year in years_dirs:
            curr_dir = pbp_dir + "/" + year + "/"
            for json_file in [curr_dir + dat for dat in os.listdir(curr_dir)]:
                # print("\n\n\n\n\n\n", "ANOTHER GAME", "\n\n\n\n\n")
                json_data = open(json_file)
                data = json.load(json_data)
                json_data.close()

                game = Game()
                game_id = data['_boxscore']['parameters']['GameID']
                game['game_id'] = game_id
                game_url = "http://stats.nba.com/stats/boxscoresummaryv2?gameid="
                game_url += game_id

                # Need Requests because we want to get the game_date from API
                yield Request(game_url, callback=self.parse_game, meta={'game': game, 'data':data}) 

    def parse_game(self, response):
        """
        Default callback used by Scrapy to process downloaded responses

        """
        data = response.meta.get('data')
        game = response.meta.get('game')
        game_info = json.loads(response.body_as_unicode())
        game_id = game['game_id']
        
        game_date = game_info['resultSets'][0]['rowSet'][0][0]
        periods = game_info['resultSets'][0]['rowSet'][0][9]
        home_team = game_info['resultSets'][0]['rowSet'][0][6]
        away_team = game_info['resultSets'][0]['rowSet'][0][7]
        
        game['game_date'] = game_date
        game['home_team_id'] = home_team
        game['visitor_team_id'] = away_team
        game['periods'] = periods 
        yield game

        box_score = data['_boxscore']
        # BOX SCORE STATS
        stat_keys = ['FT_PCT', 'FG3A', 'AST', 'PLUS_MINUS',  
                     'PTS', 'FG_PCT', 'FG3M', 'OREB', 'FTA', 'TO', 
                     'FG3_PCT', 'PF', 'FGM', 'BLK', 'STL', 'REB', 
                     'DREB', 'FTM', 'FGA']
        
                    
        player_stats = box_score['resultSets']['PlayerStats']
        
        #  PlayerGameStat and GameRoster    
        for pl_stat_dict in player_stats:
            player_id = pl_stat_dict['PLAYER_ID']
            
            roster_entry = GameRoster()
            roster_entry['game_id'] = game_id 
            roster_entry['player_id'] = player_id  
            roster_entry['team_id'] = pl_stat_dict['TEAM_ID']
            yield roster_entry         

            player_stat = PlayerGameStat()
            player_stat['game_id'] = game_id
            for stat_key in stat_keys:
                player_stat[stat_key.lower()] = pl_stat_dict[stat_key]
            player_stat['player_id'] = player_id
            # minutes separately because NBA's word 'min' is py keyword
            player_stat['minutes'] = pl_stat_dict['MIN']
            yield player_stat

        # TeamGameStat                
        team_stats = box_score['resultSets']['TeamStats']
        
        for tm_stat_dict in team_stats:
            team_stat = TeamGameStat()
            team_stat['game_id'] = game['game_id']
            for stat_key in stat_keys:
                team_stat[stat_key.lower()] = tm_stat_dict[stat_key]

            # minutes separately because NBA's word 'min' is py keyword
            team_stat['minutes'] = tm_stat_dict['MIN']

            team_stat['team_id'] = tm_stat_dict['TEAM_ID']
            yield team_stat     

        # Event Players and Matchups
        matchups = data['matchups']
        game_last_event = matchups[-1]['end_id']
        for matchup_id, matchup in enumerate(matchups):
            matchup_last_event = matchup['end_id']
            matchup_start_event = matchup['start_id']
            
            # for every event that occurred while this set of players was in
            for evt_num in range(matchup_start_event, matchup_last_event + 1):
                event_players = EventPlayers()
                event_players['game_id'] = game_id
                event_players['game_event_id'] = evt_num  
                event_players['matchup_id'] = matchup_id
                yield event_players           

            
            curr_matchup = Matchup()
            curr_matchup['game_id'] = game_id
            curr_matchup['matchup_id'] = matchup_id
            # taking time to sort them before we store them that way 
            # in app queries for five man units will be faster
            home_team = [p['id'] for p in matchup['home_players'][0]]
            away_team = [p['id'] for p in matchup['away_players'][0]]
            home_team.sort()
            away_team.sort()
            
            for i, player_id in enumerate(home_team):
                curr_matchup['home_player' + str(i+1) + '_id'] = player_id 

            for i, player_id in enumerate(away_team):
                curr_matchup['away_player' + str(i+1) + '_id'] = player_id 

            yield curr_matchup
                            

