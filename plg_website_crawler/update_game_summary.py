from bs4 import BeautifulSoup
import requests
import re
import psycopg2 as pg
import time

import cfg

class GameScore(object):
    def __init__(self, game_id, game_date, game_type, team_name, gym_name, score, opponent_score):
        self.game_id = game_id
        self.game_date = game_date
        self.game_type = game_type
        self.team_name = team_name
        self.gym_name = gym_name
        self._distribute_score(score)
        self.home = self.check_home()
        self.win = self.check_win(sum(opponent_score))
        self.sql_insert_string = self._gen_sql_string()

    def _distribute_score(self, score):
        self.ot1 = 'null'
        self.ot2 = 'null'
        self.ot3 = 'null'
        self.q1 = score[0]
        self.q2 = score[1]
        self.q3 = score[2]
        self.q4 = score[3]
        try:
            self.ot1 = score[4]
            self.ot2 = score[5]
            self.ot3 = score[6]
        except:
            pass
        self.final = sum(score)
    
    def _gen_sql_string(self):
        sql_string = f"INSERT INTO public.game_summary(\
            game_id, date, game_type, gym_id, team_id, home, win, q1, q2, q3, q4, ot1, ot2, ot3, final) VALUES(\
                {self.game_id},\
                '{self.game_date}',\
                {cfg.game_type[self.game_type]}, \
                {cfg.gym_id[self.gym_name]},\
                {cfg.team_id[self.team_name]},\
                {self.home}, \
                {self.win},\
                {self.q1},\
                {self.q2},\
                {self.q3},\
                {self.q4},\
                {self.ot1},\
                {self.ot2},\
                {self.ot3},\
                {self.final}); "
        return sql_string

    def check_home(self):
        if self.gym_name in cfg.home_gym_dict[self.team_name]:
            return True
        else:
            return False

    def check_win(self, opponent_final):
        if self.final > opponent_final:
            return True
        else:
            return False



def find_key_return_key_in_string(input_string: str, target_dict: dict):
    for key in target_dict.keys():
        if key in input_string:
            return key
    return None


for i in range(21, 22):
    url = 'https://pleagueofficial.com/game/' + str(i)
    plg_data = requests.get(url)
    soup = BeautifulSoup(plg_data.text, features='html.parser')

    # process summary info
    game_summary_info = soup.find('section', class_='pt-5 bg-black')
    game_header = game_summary_info.find(
        'div', class_='card-header bg-primary game_header')
    game_time = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}',
                          game_header.text).group()
    game_type = find_key_return_key_in_string(game_header.text, cfg.game_type)
    gym_info = find_key_return_key_in_string(game_header.text, cfg.gym_id)

    game_summary_content = game_summary_info.find('div',
                                                  class_='bg-white text-dark')
    team_info = game_summary_content.find_all(
        'div', class_='col-lg-4 col-4 align-self-center')
    left_team_name = find_key_return_key_in_string(team_info[0].text,
                                                   cfg.team_id)
    left_team_score = []
    right_team_name = find_key_return_key_in_string(team_info[1].text,
                                                    cfg.team_id)
    right_team_score = []

    quarter_info = game_summary_content.find(
        'div', class_='col-lg-4 col-4 text-center align-self-center')
    for element in quarter_info.tbody.contents:
        try:
            # filter string with Q1, Q2, Q3, Q4, OT, OT1, OT2, OT3 ...
            score_info_str = re.sub(r'Q[1-4]|OT\d{0,1}', '', element.text)
            score_info_array = score_info_str.split('\n')
            for obj in score_info_array:
                if re.search(r'\d{1,2}', obj) is not None:
                    # score is found, check left_team or right team
                    if len(left_team_score) == len(right_team_score):
                        left_team_score.append(int(obj))
                    else:
                        right_team_score.append(int(obj))
        except:
            pass
    left_team = GameScore(i, game_time, game_type, left_team_name, gym_info, left_team_score, right_team_score)
    right_team = GameScore(i, game_time, game_type, right_team_name, gym_info, right_team_score, left_team_score)
    
    try:
        conn = pg.connect(database=cfg.database, user=cfg.user, password=cfg.password,
                            host=cfg.host, port=cfg.port)
    except Exception as e:
        print(e)

    cur = conn.cursor()
    try:
        cur.execute(left_team.sql_insert_string)
        cur.execute(right_team.sql_insert_string)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
    
    cur.close()
    conn.close()
    time.sleep(3)