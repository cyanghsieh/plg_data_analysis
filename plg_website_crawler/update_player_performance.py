from bs4 import BeautifulSoup
import requests
import re
import psycopg2 as pg
import time

import cfg

class PlayerPerformance(object):
    def __init__(self, game_id, team_name, header, stat):
        self._header = header
        self._stat = stat
        self.player_name = self._get_player_name()
        self.start_up = self._identify_startup()
        self.final_stat = self._trans_datatype()
        self.game_id = game_id
        self.team_id = cfg.team_id[team_name]
        self.sql_insert_string = self._gen_sql_string()



    def _gen_sql_string(self):
        sql_string = f"INSERT INTO public.player_stats( \
            game_id, team_id, jersey_number, start_lineup, name, duration, twoptsmade, twoptsshot, twoptspct, threeptsmade, threeptsshot, threeptspct, ftmade, ftshot, ftpct, pts, reb, oreb, dreb, ast, stl, blk, tover, foul, eff, ud, tspct, usgpct, efgpct) VALUES( \
                {self.game_id}, \
                {self.team_id},"
        for i in self.final_stat:
            if type(i) is str:
                sql_string = sql_string + f"'{i}',"
            elif i is None:
                sql_string = sql_string + 'null,'
            else:
                sql_string = sql_string + f"{i},"
        sql_string = sql_string[:-1] + ");"
        return sql_string





    def _identify_startup(self):
        if self._stat[1] != '':
            return True
        else:
            return False    
    def _get_player_name(self):
        for i in range(len(self._header)):
            if self._header[i] == 'player':
                return self._stat[i].replace('\n', '')
                
    def _trans_datatype(self):
        new_stat = []
        for idx in range(len(self._stat)):
            idx_data = None
            if idx == 1:
                # startup
                if self._stat[idx] != '':
                    idx_data = True
                else:
                    idx_data = False
            elif idx == 2:
                # name
                # self.player_name = self._stat[idx].replace('\n', '')
                idx_data = self._stat[idx].replace('\n', '')
            elif idx == 3:
                # trans time to second
                try:
                    minute_data = float(self._stat[idx].split(':')[0])
                    second_data = float(self._stat[idx].split(':')[1])
                    idx_data = minute_data * 60 + second_data
                except:
                    # DNP
                    idx_data = None
                    
            else:
                if '%' in self._stat[idx]:
                    try:
                        idx_data = float(self._stat[idx].replace('%', '')) / 100
                        # idx_data = float(self._stat[idx - 2]) / float(self._stat[idx - 1])
                    except:
                        idx_data = None
                    
                elif self._stat[idx] == '':
                    idx_data = None
                else:
                    idx_data = float(self._stat[idx])
            new_stat.append(idx_data)
        return new_stat
                

def find_key_return_key_in_string(input_string: str, target_dict: dict):
    for key in target_dict.keys():
        if key in input_string:
            return key
    return None


def extract_player_performance(input_soup):
    header = []
    index_to_be_split = []
    header_info = input_soup.thead.tr.find_all('th')
    for idx in range(len(header_info)):
        header.append(cfg.stat_header_dict[header_info[idx].text])
        # split 2pt, 3pt, ft
        if header_info[idx].text == '二分':
            index_to_be_split.append(idx)
            header.append('twoptsshot')
        elif header_info[idx].text == '三分':
            index_to_be_split.append(idx)
            header.append('threeptsshot')
        elif header_info[idx].text == '罰球':
            index_to_be_split.append(idx)
            header.append('ftshot')

    players_stat = input_soup.tbody.find_all('tr')
    for player in players_stat:
        stat_info = []
        for i in range(len(player.find_all('td'))):
            element_string = player.find_all('td')[i].text
            if i in index_to_be_split:
                try:
                    stat_info.append(element_string.split('-')[0])
                    stat_info.append(element_string.split('-')[1])
                except:
                    # when DNP
                    stat_info.append('')
            else:
                stat_info.append(element_string)
        # stat complete
        player_obj = PlayerPerformance(CURRENT_GAME_ID, CURRENT_TEAM, header, stat_info)
        
        try:
            conn = pg.connect(database=cfg.database, user=cfg.user, password=cfg.password,host=cfg.host, port=cfg.port)
        except Exception as e:
            print(e)

        cur = conn.cursor()
        try:
            cur.execute(player_obj.sql_insert_string)
        except Exception as e:
            print(e)
        finally:
            conn.commit()
    
    cur.close()
    conn.close()


for i in range(21, 22):
    url = 'https://pleagueofficial.com/game/' + str(i)
    plg_data = requests.get(url)
    soup = BeautifulSoup(plg_data.text, features='html.parser')

    # process summary info
    player_stat_info = soup.find('section', class_='pt-2').find('div', class_='tab-pane fade show active')
    team_array = player_stat_info.find_all('h1')
    left_team = team_array[0].text
    right_team = team_array[1].text
    team_stat_array = player_stat_info.find_all('div')
    left_team_stat = team_stat_array[0]
    right_team_stat = team_stat_array[1]

    CURRENT_GAME_ID = i
    CURRENT_TEAM = left_team
    extract_player_performance(left_team_stat)
    CURRENT_TEAM = right_team
    extract_player_performance(right_team_stat)
    time.sleep(1)


    # print('done')


    # game_summary_info = soup.find('section', class_='pt-5 bg-black')
    # game_header = game_summary_info.find(
    #     'div', class_='card-header bg-primary game_header')
    # game_time = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}',
    #                       game_header.text).group()
    # game_type = find_key_return_key_in_string(game_header.text, cfg.game_type)
    # gym_info = find_key_return_key_in_string(game_header.text, cfg.gym_id)

    # game_summary_content = game_summary_info.find('div',
    #                                               class_='bg-white text-dark')
    # team_info = game_summary_content.find_all(
    #     'div', class_='col-lg-4 col-4 align-self-center')
    # left_team_name = find_key_return_key_in_string(team_info[0].text,
    #                                                cfg.team_id)
    # left_team_score = []
    # right_team_name = find_key_return_key_in_string(team_info[1].text,
    #                                                 cfg.team_id)
    # right_team_score = []

    # quarter_info = game_summary_content.find(
    #     'div', class_='col-lg-4 col-4 text-center align-self-center')
    # for element in quarter_info.tbody.contents:
    #     try:
    #         # filter string with Q1, Q2, Q3, Q4, OT, OT1, OT2, OT3 ...
    #         score_info_str = re.sub(r'Q[1-4]|OT\d{0,1}', '', element.text)
    #         score_info_array = score_info_str.split('\n')
    #         for obj in score_info_array:
    #             if re.search(r'\d{1,2}', obj) is not None:
    #                 # score is found, check left_team or right team
    #                 if len(left_team_score) == len(right_team_score):
    #                     left_team_score.append(int(obj))
    #                 else:
    #                     right_team_score.append(int(obj))
    #     except:
    #         pass
    # left_team = GameScore(i, game_time, game_type, left_team_name, gym_info, left_team_score, right_team_score)
    # right_team = GameScore(i, game_time, game_type, right_team_name, gym_info, right_team_score, left_team_score)
    
    # try:
    #     conn = pg.connect(database=cfg.database, user=cfg.user, password=cfg.password,
    #                         host=cfg.host, port=cfg.port)
    # except Exception as e:
    #     print(e)

    # cur = conn.cursor()
    # try:
    #     cur.execute(left_team.sql_insert_string)
    #     cur.execute(right_team.sql_insert_string)
    # except Exception as e:
    #     print(e)
    # finally:
    #     conn.commit()
    
    # cur.close()
    # conn.close()
    # time.sleep(3)