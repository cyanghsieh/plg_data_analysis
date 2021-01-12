host = '*.*.*.*'
port = '5432'
database = 'PLG'
user = '****'
password = '**********'

game_type = {'熱身賽': 1, '例行賽': 2, '季後賽': 3}
gym_id = {'新竹縣體育館': 1, '臺北和平籃球館': 2, '彰化縣立體育館': 3, '桃園市立綜合體育館': 4, '臺體大體育館': 5}
team_id = {'臺北富邦勇士': 1, '桃園領航猿': 2, '新竹街口攻城獅': 3, '福爾摩沙台新夢想家': 4}
home_gym_dict = {
    '臺北富邦勇士': ['臺北和平籃球館'],
    '桃園領航猿': ['桃園市立綜合體育館'],
    '新竹街口攻城獅': ['新竹縣體育館'],
    '福爾摩沙台新夢想家': ['福爾摩沙台新夢想家', '臺體大體育館']
}

stat_header_dict = {
    '#': 'jersey_number',
    '先發': 'start_lineup',
    '球員': 'player',
    '時間': 'duration',
    '二分': 'twoptsmade',
    '二分%': 'twoptspct',
    '三分': 'threeptsmade',
    '三分%': 'threeptspct',
    '罰球': 'ftmade',
    '罰球%': 'ftpct',
    '得分': 'pts',
    '籃板': 'reb',
    '攻板': 'oreb',
    '防板': 'dreb',
    '助攻': 'ast',
    '抄截': 'stl',
    '阻攻': 'blk',
    '失誤': 'tov',
    '犯規': 'pf',
    'EFF': 'EFF',
    '+/-': 'ud',
    'TS%': 'tspct',
    'USG%': 'usgpct',
    'EFG%': 'efgpct'
}
