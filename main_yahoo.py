import pandas as pd
from roster import Roster
from tradevalue import TradeValue

LEAGUE_ID_LIST = [55598, 55617]

def col_replace(df, column_name):
    df[column_name] = df[column_name].str.replace('.', '', regex=False)
    df[column_name] = df[column_name].str.replace('Kenneth', 'Ken', regex=False)
    df[column_name] = df[column_name].str.replace(' Jr', '', regex=False)
    df[column_name] = df[column_name].str.rstrip(' III')
    df[column_name] = df[column_name].str.rstrip(' II')
    df[column_name] = df[column_name].str.replace(' Sr', '', regex=False)
    return df

def df_to_csv(leagueid):
    team1 = Roster(leagueid=leagueid)
    TradeValue_Class = TradeValue("https://www.thescore.com/nfl/news/3133428/fantasy-trade-value-chart-week-12")
    TradeValue_df = col_replace(TradeValue_Class.all_dfs, 'Player')
    team1_df = col_replace(team1.roster_df, 'player_name')
    all_df = pd.merge(TradeValue_df,team1_df,left_on='Player',right_on='player_name',how='left')
    all_df.sort_values('Value', ascending=False).to_csv(f'{leagueid}.csv', sep=',')
    return all_df

def main():
    for league_id in LEAGUE_ID_LIST():
        df_to_csv(league_id)
    
if __name__ == "__main__":
    main()