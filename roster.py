# -*- coding: utf-8 -*-

from yahoologin import yahoologin
import csv
import pandas as pd
class Roster:
    def __init__(self, leagueid, numteams = 10):
        self.leagueid = leagueid
        self.numteams = numteams
        self.updateroster()

    def getgameid(self, game='nfl'):
        oauth = yahoologin()
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/game/' + game
        response = oauth.session.get(url, params={'format': 'json'})
        data = response.json()
        return data['fantasy_content']['game'][0]['game_id']

    def updateroster(self, league='nfl'):
        oauth = yahoologin()
        leagueid = self.leagueid
        numteams = self.numteams
        gameid = self.getgameid(league)
        roster_list = list()
        for team in range(1, numteams+1): #assumes 10-team league
            url = 'https://fantasysports.yahooapis.com/fantasy/v2/team/'+str(gameid)+'.l.'+str(leagueid)+'.t.'+str(team)+'/players/percent_owned'
            response = oauth.session.get(url, params={'format': 'json'})
            data = response.json()
            playercount = 0
            for item in (data["fantasy_content"]["team"][1]["players"]):
                if 'count' not in item:
                    try:
                        #print(item)
                        percentowned = data["fantasy_content"]["team"][1]["players"][item]["player"][1]['percent_owned'][1]['value']
                        player_id = data["fantasy_content"]["team"][1]["players"][item]["player"][0][1]["player_id"]
                        player_name = data["fantasy_content"]["team"][1]["players"][item]["player"][0][2]["name"]["full"]
                        team_name = data["fantasy_content"]["team"][0][2]["name"]
                    except:
                        print(str(playercount),numteams)
                    finally:
                        roster_list.append([player_name, team_name, percentowned])
        
        self.roster_df = pd.DataFrame(roster_list,columns=['player_name','team_name','percent_owned'])