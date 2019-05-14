
# Steam Scrapper - testing out MariaDB inserts and JSON parsing

import json
import pandas as pd
import configparser as cp
import requests
import mysql.connector as mariadb

def get_homedir():
    # parse from steam.cfg, returns path string WITH trailing '/'

    config = cp.ConfigParser()
    config.readfp(open(r'/home/code/steam_scrapper/steam.cfg'))
    homedir = config.get('APPLIST', 'HOME', fallback=None)
    if homedir == None:
        return 'no homedir variable found!'
    if homedir[-1] != '/':
        return homedir + '/'
    else:
        return homedir

def get_web_data():
    # downloads data from the web
    resp = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v2')
    htmltext = resp.text
    return htmltext

def create_dataframe(input_list):
    df = pd.DataFrame(input_list)
    print(df.head())
    return df

def insert_mariadb(username, db, input_list):
    mariadb_conn = mariadb.connect(user=username, password='123', database=db)
    cursor = mariadb_conn.cursor()

    print('inserting into mariadb mydb.test table...')
    for element in input_list:
        cursor.execute('INSERT INTO test (appid, name) VALUES (%s, %s)',(element['appid'], element['name']))

    mariadb_conn.commit()
    mariadb_conn.close()

json_data = json.loads(get_web_data())
appid_list = json_data['applist']['apps']

# Try inserting into MariaDB!
insert_mariadb('root', 'mydb', appid_list)

# Try creating a dataframe!
create_dataframe(appid_list)

