# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

# BOT_NAME = 'player_id'

SPIDER_MODULES = ['nba_app.spiders']


DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'shanefenske',  # fill in your username here
    'password': '',  # fill in your password here
    'database': 'nba'
}
