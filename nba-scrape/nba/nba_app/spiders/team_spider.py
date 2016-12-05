#! -*- coding: utf-8 -*-

"""

"""
from scrapy import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from nba_app.items import Team
import json

from ..settings import DATABASE
from ..tools import string_height_to_inches
from ..teams import team_name_dict
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text

class NBATeamSpider(BaseSpider):
    """
    Make request for every NBA team
    """
    name = "teams"
    
    # return every team in nba
    start_urls = ["http://stats.nba.com/stats/commonteamyears?LeagueID=00"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'nba_app.pipelines.TeamPipeline': 300,
        }
    }


    def parse(self, response):
        """
        Default callback used by Scrapy to process downloaded responses

        """
        data = json.loads(response.body_as_unicode())

        for row in data['resultSets'][0]['rowSet'][:30]:
            team = Team()
            team_id = row[1] 
            print(row, "\n", team_id, type(team_id))
            team['team_id'] = row[1] 
            team['abbreviation'] = row[4]
            team["name"] = team_name_dict[team_id]
            yield team
