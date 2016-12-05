#! -*- coding: utf-8 -*-

"""

"""
from scrapy import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from nba_app.items import Player
import json

from ..settings import DATABASE
from ..tools import string_height_to_inches
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text

class NBAPlayerSpider(BaseSpider):
    """
    Make request for every NBA player ever
    """
    name = "players"
    
    # return every player to play in nba
    start_urls = ["http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=2015-16"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'nba_app.pipelines.PlayerPipeline': 300,
        }
    }


    def parse(self, response):
        """
        Default callback used by Scrapy to process downloaded responses

        """
        data = json.loads(response.body_as_unicode())

        for row in data['resultSets'][0]['rowSet']:
            player = Player()
            print("processing", row[1], row[0])
            player_id = row[0] 
            player['player_id'] = player_id
            player['roster_status'] = row[3]
            player['from_year'] = row[4]
            player['to_year'] = row[5]
            player['team_id'] = row[7]
            info_url = "http://stats.nba.com/stats/commonplayerinfo?PlayerID="
            player_info_url = info_url + str(player_id)

            yield Request(player_info_url, callback=self.parse_player_info, meta={'player': player}) 

        


#     # generate url for every player in our player_ids list
#     player_info_url = "http://stats.nba.com/stats/commonplayerinfo?PlayerID="
    
#     start_urls = ["http://stats.nba.com/stats/commonplayerinfo?PlayerID=" + str(player_id) for player_id in player_ids]

#     # TODO DELETE
#     start_urls = start_urls[:1]

    def parse_player_info(self, response):
        """
        Parse each player's player info json

        """
        player = response.meta.get('player')
        data = json.loads(response.body_as_unicode())
        header = data['resultSets'][0]['headers']

        # TODO delete? all caps is ok?
        # header = [h.lower() if type(h) == type("") else h for h in header]
        
        values = data['resultSets'][0]['rowSet'][0]
        info_dict = {pair[0]:pair[1] for pair in zip(header,values)}

        # these are the columns we want to save from the 
        # stats/commonplayerinfo request
        info_cols = ["FIRST_NAME","LAST_NAME","BIRTHDATE","SCHOOL","COUNTRY","LAST_AFFILIATION", 
        "WEIGHT","SEASON_EXP","JERSEY","POSITION","DLEAGUE_FLAG","DRAFT_YEAR",
        "DRAFT_ROUND","DRAFT_NUMBER"]

        for col in info_cols:
            player[col.lower()] = info_dict[col]

        player['height'] = string_height_to_inches(info_dict['HEIGHT'])
        yield player
        # print("\n\n\n\n\n\n", data['resultSets'][0]['headers'], "\n\n\n\n\n\n", data['resultSets'][0]['rowSet'], "\n\n\n\n\n\n")

