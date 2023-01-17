from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd

class TradeValue:
    def get_links(self):
        base_link = self.base_link
        req = Request(base_link)
        html_page = urlopen(req)

        soup = BeautifulSoup(html_page, "lxml")

        links = {}
        links['base'] = base_link

        for link in soup.find_all('a'):
            if link.get('href') is not None:
                if link.get('href').startswith("https://www.thescore.com/news"):
                    link_text = link.get_text()
                    link_value = link.get('href')
                    links[link_text] = link_value
        self.links = links

    def get_trade_value_dfs(self):
        dfs_list = []
        for value in self.links.values():
            pd.read_html(value)
            dfs_list.append(pd.read_html(value)[0])
        all_dfs = pd.concat(dfs_list)
        all_dfs['Value'] = all_dfs['PPR'].fillna(0) + all_dfs['1QB'].fillna(0)
        
        self.all_dfs = all_dfs[['Player','Value']]
    
    def __init__(self, base_link):
        self.base_link = base_link
        self.get_links()
        self.get_trade_value_dfs()