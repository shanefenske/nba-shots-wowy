# nba-shots-wowy
The nbawowy of shotchart sites
 
/nba_app contains Flask app
/nba_scrape contains scrapy spiders used to parse NBA API returns and funnel them into Postgres database.
/nba_scrape/pbp contains example of the raw play by play files I used to assign lineups to shots


## Tables
                                                           Table "public.players"
      Column      |       Type        |                          Modifiers                          | Storage  | Stats target | Description 
------------------+-------------------+-------------------------------------------------------------+----------+--------------+-------------
 player_id        | integer           | not null default nextval('players_player_id_seq'::regclass) | plain    |              | 
 first_name       | character varying |                                                             | extended |              | 
 last_name        | character varying |                                                             | extended |              | 
 birthdate        | date              |                                                             | plain    |              | 
 school           | character varying |                                                             | extended |              | 
 country          | character varying |                                                             | extended |              | 
 last_affiliation | character varying |                                                             | extended |              | 
 height           | character varying |                                                             | extended |              | 
 weight           | character varying |                                                             | extended |              | 
 season_exp       | character varying |                                                             | extended |              | 
 jersey           | character varying |                                                             | extended |              | 
 position         | character varying |                                                             | extended |              | 
 dleague_flag     | character varying |                                                             | extended |              | 
 draft_year       | character varying |                                                             | extended |              | 
 draft_round      | character varying |                                                             | extended |              | 
 draft_number     | character varying |                                                             | extended |              | 
 roster_status    | character varying |                                                             | extended |              | 
 from_year        | character varying |                                                             | extended |              | 
 to_year          | character varying |                                                             | extended |              | 
 team_id          | character varying |                                                             | extended |              | 
Indexes:
    "players_pkey" PRIMARY KEY, btree (player_id)


                                                        Table "public.teams"
    Column    |       Type        |                        Modifiers                        | Storage  | Stats target | Description 
--------------+-------------------+---------------------------------------------------------+----------+--------------+-------------
 team_id      | integer           | not null default nextval('teams_team_id_seq'::regclass) | plain    |              | 
 abbreviation | character varying |                                                         | extended |              | 
 name         | character varying |                                                         | extended |              | 
Indexes:
    "teams_pkey" PRIMARY KEY, btree (team_id)


                                                    Table "public.games"
     Column      |  Type   |                        Modifiers                        | Storage | Stats target | Description 
-----------------+---------+---------------------------------------------------------+---------+--------------+-------------
 game_id         | integer | not null default nextval('games_game_id_seq'::regclass) | plain   |              | 
 game_date       | date    |                                                         | plain   |              | 
 periods         | integer |                                                         | plain   |              | 
 home_team_id    | integer |                                                         | plain   |              | 
 visitor_team_id | integer |                                                         | plain   |              | 
Indexes:
    "games_pkey" PRIMARY KEY, btree (game_id)


                           Table "public.matchups"
     Column      |  Type   | Modifiers | Storage | Stats target | Description 
-----------------+---------+-----------+---------+--------------+-------------
 game_id         | integer | not null  | plain   |              | 
 matchup_id      | integer | not null  | plain   |              | 
 home_player1_id | integer |           | plain   |              | 
 home_player2_id | integer |           | plain   |              | 
 home_player3_id | integer |           | plain   |              | 
 home_player4_id | integer |           | plain   |              | 
 home_player5_id | integer |           | plain   |              | 
 away_player1_id | integer |           | plain   |              | 
 away_player2_id | integer |           | plain   |              | 
 away_player3_id | integer |           | plain   |              | 
 away_player4_id | integer |           | plain   |              | 
 away_player5_id | integer |           | plain   |              | 
Indexes:
    "matchups_pkey" PRIMARY KEY, btree (game_id, matchup_id)


                               Table "public.shots"
       Column        |  Type   | Modifiers | Storage | Stats target | Description 
---------------------+---------+-----------+---------+--------------+-------------
 game_id             | integer | not null  | plain   |              | 
 game_event_id       | integer | not null  | plain   |              | 
 player_id           | integer |           | plain   |              | 
 loc_x               | integer |           | plain   |              | 
 loc_y               | integer |           | plain   |              | 
 shot_made_flag      | integer |           | plain   |              | 
 shot_attempted_flag | integer |           | plain   |              | 
Indexes:
    "shots_pkey" PRIMARY KEY, btree (game_id, game_event_id)


                        Table "public.event_players"
    Column     |  Type   | Modifiers | Storage | Stats target | Description 
---------------+---------+-----------+---------+--------------+-------------
 game_id       | integer | not null  | plain   |              | 
 game_event_id | integer | not null  | plain   |              | 
 matchup_id    | integer |           | plain   |              | 
Indexes:
    "event_players_pkey" PRIMARY KEY, btree (game_id, game_event_id)


                           Table "public.matchups"
     Column      |  Type   | Modifiers | Storage | Stats target | Description 
-----------------+---------+-----------+---------+--------------+-------------
 game_id         | integer | not null  | plain   |              | 
 matchup_id      | integer | not null  | plain   |              | 
 home_player1_id | integer |           | plain   |              | 
 home_player2_id | integer |           | plain   |              | 
 home_player3_id | integer |           | plain   |              | 
 home_player4_id | integer |           | plain   |              | 
 home_player5_id | integer |           | plain   |              | 
 away_player1_id | integer |           | plain   |              | 
 away_player2_id | integer |           | plain   |              | 
 away_player3_id | integer |           | plain   |              | 
 away_player4_id | integer |           | plain   |              | 
 away_player5_id | integer |           | plain   |              | 
Indexes:
    "matchups_pkey" PRIMARY KEY, btree (game_id, matchup_id)
