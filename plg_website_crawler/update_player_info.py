from bs4 import BeautifulSoup
import requests
import re
import psycopg2 as pg
import time

import cfg

class player(object):
    def __init__(self, name_TW, name_EN, height, weight, jersey_number, dob, position):
        self.name_TW = name_TW
        self.name_EN = name_EN
        self.height = height
        self.weight = weight
        self.jersey_number = jersey_number
        self.dob = dob
        self.position = position
        self.print_data()
    
    def print_data(self):
        result = f"{self.name_TW}-{self.name_EN}-{self.position}-{self.dob}-{self.height}-{self.weight}"
        print(result)

# player1 = player('A','B',195,65,12,'1983-10-10','F')
for i in range(1, 200):
    url = 'https://pleagueofficial.com/player/'+str(i)
    plg_data = requests.get(url)
    soup = BeautifulSoup(plg_data.text, features='html.parser')
    height = None
    weight = None
    jersey_number = None
    pos = None
    dob = None
    name_TW = None
    name_EN = None
    player_info_array = []
    
    try:
        player_raw_info = soup.find('section', class_='pt-md-5 section_player').text
        for element in player_raw_info.split('\n'):
            if element != '':
                player_info_array.append(element)

        # get jersey number and pos
        jersey_number = int(re.search(r'\d+',(player_info_array[0].split('|'))[1]).group())
        pos = (player_info_array[0].split('|'))[2].replace(' ', '')
        
        # get player name
        player_nameTW = player_info_array[1]
        player_nameEN = player_info_array[2]
        for element in soup.p.contents:
            if '身高' in str(element):
                height = float(re.search(r'\d+', element.text).group())
            elif '體重' in str(element):
                weight = float(re.search(r'\d+', element.text).group())
            elif '生日' in str(element):
                dob = re.search(r'\d{4}-\d{2}-\d{2}', element.text).group()

        current_player = player(player_nameTW, player_nameEN, height, weight, jersey_number, dob, pos)

        # insert into database
        try:
            conn = pg.connect(database=cfg.database, user=cfg.user, password=cfg.password,
                            host=cfg.host, port=cfg.port)
        except Exception as e:
            print(e)

        cur = conn.cursor()
        execute_sql_script = f"INSERT INTO player(id,name_tw,name_en,jersey_number,position,height,weight,dob)\
            VALUES({i}, '{player_nameTW}', '{player_nameEN}', {jersey_number}, '{pos}', {height}, {weight}, '{dob}');"
        try:
            cur.execute(execute_sql_script)
        except Exception as e:
            print(e)
        finally:
            conn.commit()    
    except Exception as e:
        print(f"{e} --- {url}")

    cur.close()
    conn.close()
    time.sleep(3)