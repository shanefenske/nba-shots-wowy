# #! -*- coding: utf-8 -*-

"""

"""
from scrapy import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from nba_app.items import Shot
import json

from ..settings import DATABASE
from ..tools import string_height_to_inches
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text

class ShotSpider(BaseSpider):
    """
    Make request for every Shot take in 2015-16
    """
    name = "shots"

    # 1996-97 is first season with shot charts online makes list of
    # list of strings of api format years ie. [1996-97, 1997-98, .. 2015-2016]
    years = [str(i) + "-" + str(i+1)[2:] for i in range(1996,2016)]

    custom_settings = {
        'ITEM_PIPELINES': {
            'nba_app.pipelines.ShotPipeline': 300,
        }
    }    

    def start_requests(self):
        """
        Override start_requests because we want dynamic start_url generation
        """
        # TODO: SPEED THIS UP 2X+ BY GRABBING_FROM_YEAR AND TO_YEAR FROM DB
        # AND ONLY MAKING REQUEST IF YEAR IS WITHIN RANGE(FROM_YEAR, TO_YEAR)
        eng = create_engine(URL(**DATABASE))
        connection = eng.connect() 
        id_tups = connection.execute("select player_id from players;").fetchall()
        players = [tup[0] for tup in id_tups]
        connection.close()
        start_urls = [self.get_shot_url(player_id, year) for player_id in players for year in self.years]
        
        for url in start_urls:
            yield Request(url, self.parse)


    def parse(self, response):
        """
        Default callback used by Scrapy to process downloaded responses

        """        
        # these are the columns we want to save from the 
        # shotchartdetail API request
        shot_cols = ["GAME_ID","GAME_EVENT_ID","PLAYER_ID", "LOC_X","LOC_Y", 
                     "SHOT_ATTEMPTED_FLAG","SHOT_MADE_FLAG"]

        data = json.loads(response.body_as_unicode())
        shots = data['resultSets'][0]['rowSet'] 
        if shots != []:
            header = data['resultSets'][0]['headers']
            for shot in shots:
                shot_dict = {pair[0]:pair[1] for pair in zip(header,shot)}

                shot = Shot()

                for col in shot_cols:
                    shot[col.lower()] = shot_dict[col]

                yield shot

    def get_shot_url(self, player_id, year):
        url = "http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS="\
        + year + "&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&GameID="\
        + "&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month"\
        + "=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0"\
        + "&PlayerID=" + str(player_id) + "&PlusMinus=N&Position=&Rank=N&"\
        + "RookieYear=&Season=" + year + "&SeasonSegment=&SeasonType=Regular+"\
        + "Season&TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails="\
        + "0&showShots=1&showZones=0&PlayerPosition"

        return url
