import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import dota2api
import os

api = dota2api.Initialise("8AC9317F6C4C6AA98EECEC8638314A11")
hist = api.get_match_history(account_id=107940251, matches_requested=10)


def pull_match_id(acc_id, n):
    hist = api.get_match_history(account_id=acc_id, matches_requested=n)
    match_info = {"match_id":[np.nan], "account_id":[np.nan], "hero_id":[np.nan], "player_slot":[np.nan]}
    match_info = pd.DataFrame(match_info)
    for i in range(0, len(hist['matches'])):
        for j in range(0, len(hist['matches'][i]['players'])):
            temp_acc = hist['matches'][i]['players'][j]
            account_id = temp_acc['account_id']
            if account_id == acc_id:
                match_id = hist['matches'][i]['match_id']
                account_id = int(acc_id)
                hero_id = temp_acc["hero_id"]
                player_slot = temp_acc["player_slot"]
                if player_slot < 5:
                    side = "Radiant"
                else:
                    side = "Dire"
                final_data = {"match_id":match_id, "account_id":acc_id, "hero_id":hero_id, "player_slot":player_slot, "side":side}

                match_info = match_info.append(final_data, ignore_index=True)

    return match_info.dropna()

### internal function

def get_data_match(match_json):
    """ get match_data from match_json object from dota2api get_match_details function
    Args:
        match_json: object of dota2api get_match_details function
    Returns:
        pandas DataFrame
    """
    invalid1 = {"players", "picks_bans"}
    match_data = {x:match_json[x] for x in match_json if x not in invalid1}
    df1 = pd.DataFrame(match_data, index=[0])
    return(df1)


### internal function
def get_data_player(player_id, match_json):
    """ get player_data from match_json object from dota2api get_match_details function
        with specific player_id

    Args:
        player_id: id of player, for example 10790251
        match_json: object of dota2api get_match_details function
    Returns:
        pandas DataFrame
    """
    invalid2 = {"ability_upgrades", "account_id"}
    player = match_json['players']
    for j in range(0, len(player)):
        if player[j]['account_id'] == player_id:
            player_data = {x: player[j][x] for x in player[j] if x not in invalid2}
            df2 = pd.DataFrame(player_data, index=[0])
    return(df2)



def get_match_final(data):
    """ Wrapper for get_data_match and get_data_player, concatenate 2 dataframe into single DataFrame
        with hero stats data
    Args:
        data: object from pull_match_id function
    Returns:
        pandas DataFrame
    """
    final_data = pd.DataFrame()

    # Load hero_stats_2.csv data
    root_path = os.getcwd()
    data_path = "Dota2Project/Data/dota_hero_stats_2.csv"
    hero_path = os.path.join(root_path, data_path)
    hero_stats = pd.read_csv(hero_path)

    for i in range(0, len(data)):
        id = int(data.iloc[i,2])
        player_id = data.iloc[i,0]

        match_json = api.get_match_details(id)

        temp1 = get_data_match(match_json)
        temp2 = get_data_player(player_id, match_json)

        df = pd.concat([temp1, temp2], axis=1)

        # df = pd.concat([df, data.iloc[i,:]], axis=1)
        final_data = final_data.append(df, ignore_index=True)

        # Exctract hero stats and concatenate to pandas DataFrame
        hero_id = final_data.hero_id.values[0]
        hero_data = hero_stats[hero_stats.id == hero_id]

        # Final DataFrame
        final_data_hero = pd.concat([final_data, hero_data])
        # final_data = pd.concat([final_data, data], axis=1)

    # return final_data
    return final_data_hero

match_data = pull_match_id(acc_id=181798082, n=10)
player_data = get_match_final(match_data)

player_data.columns.values
ab  = player_data.head(1).hero_id
ab.values[0]atrd
### Adding more columns to the data array


def clean_data(match_data, player_data):
    clean = pd.concat([match_data.reset_index(), player_data], axis=1)
    results = []
    # Path for hero file
    for i in range(0, len(clean)):
        if clean.iloc[i, 59]==1 and clean.iloc[i,5]=='Radiant':
            results.append(1)
        elif clean.iloc[i,59]!=1 and clean.iloc[i,5]=='Dire':
            results.append(1)
        else:
            results.append(0)
        hero_id = clean.iloc[i, 2]

    clean['Results'] = results
    return clean


### Final Function
def final_data(acc_id, n):
    match_data = pull_match_id(acc_id, n)
    player_data = get_match_final(match_data)
    final_df = clean_data(match_data, player_data)
    return(final_df)


col_type1 = ['match_id', 'year', 'month', 'day', 'hour', 'side', 'start_time',
                'duration','hero_id', 'radiant_win','kills', 'deaths', 'assists',]

test1.columns.values



### UNIT_TESTING
test0 = pull_match_id(181798082, 10)
test1 = get_match_final(test0)
test2 = clean_data(test0, test1)

test2.columns.values
test2.head()
test3 = test2[col_type1]

final1 = final_data(181798082, 10)
final1

### Analysis
wins = len(test2[test2['Results']==1])
wins_pct = round(wins/len(test2),3)
wins_pct

losses = len(test2[test2['Results']==0])
losses_pct = 1 - wins_pct

radiant_wins = test2['radiant_win'].value_counts()
test3.head(2)


### Converting to year month date
test3['duration'] = round(test3['duration']/60, 3)
print(test3.index)



year = []
month = []
day = []
hour = []

a = datetime.datetime.fromtimestamp(test3['start_time'][1])
a


for ix in test3['start_time'].index:
    ts = datetime.datetime.fromtimestamp(test3['start_time'][ix])
    year.append(ts.year)
    month.append(ts.month)
    day.append(ts.day)
    hour.append(ts.hour)

test3.insert(3, 'year', year)
test3.insert(3, 'month', month)
test3.insert(3, 'day', day)
test3.insert(3, 'hour', hour)




test3.head(2)

test3.rename(columns={"hero_id":"id"})




print("done")
