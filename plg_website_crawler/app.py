import re
import time

from flask import Flask, render_template
import psycopg2 as pg
import requests

import cfg

app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    query_string = "SELECT * FROM standings;"
    query_result = postgresql_query(query_string)

    return render_template("index.html", results=query_result)


@app.route('/average_ast')
def average_ast():
    query_string = "SELECT team_name, player_name, play, round(avg_ast::numeric,3), round((avg_ast*play)::numeric,0) FROM regular_season_stat_ranking ORDER BY avg_ast DESC LIMIT 15;"
    query_result = postgresql_query(query_string)
    team = []
    name = []
    ast = []
    total_ast = []
    for item in query_result:
        team.append(item[0])
        name.append(item[1])
        ast.append("%.3f" % float(item[3]))
        total_ast.append(int(item[4]))

    return render_template("average_ast.html",
                           results=query_result,
                           team=team,
                           name=name,
                           ast=ast,
                           totalAst=total_ast)


@app.route('/average_blk')
def average_blk():
    query_string = "SELECT team_name, player_name, play, round(avg_blk::numeric,3), round((avg_blk*play)::numeric,0) FROM regular_season_stat_ranking ORDER BY avg_blk DESC LIMIT 15;"
    query_result = postgresql_query(query_string)
    team = []
    name = []
    blk = []
    total_blk = []
    for item in query_result:
        team.append(item[0])
        name.append(item[1])
        blk.append("%.3f" % float(item[3]))
        total_blk.append(int(item[4]))

    return render_template("average_blk.html",
                           results=query_result,
                           team=team,
                           name=name,
                           blk=blk,
                           totalBlk=total_blk)


@app.route('/average_pts')
def average_pts():
    query_string = "SELECT team_name, player_name, play, round(avg_pts::numeric,3), round((avg_pts*play)::numeric,0) FROM regular_season_stat_ranking ORDER BY avg_pts DESC LIMIT 15;"
    query_result = postgresql_query(query_string)
    team = []
    name = []
    score = []
    total_score = []
    for item in query_result:
        team.append(item[0])
        name.append(item[1])
        score.append("%.3f" % float(item[3]))
        total_score.append(int(item[4]))

    return render_template("average_pts.html",
                           results=query_result,
                           team=team,
                           name=name,
                           score=score,
                           totalScore=total_score)


@app.route('/average_reb')
def average_reb():
    query_string = "SELECT team_name, player_name, play, round(avg_reb::numeric,3), round((avg_reb*play)::numeric,0) FROM regular_season_stat_ranking ORDER BY avg_reb DESC LIMIT 15;"
    query_result = postgresql_query(query_string)
    team = []
    name = []
    reb = []
    total_reb = []
    for item in query_result:
        team.append(item[0])
        name.append(item[1])
        reb.append("%.3f" % float(item[3]))
        total_reb.append(int(item[4]))

    return render_template("average_reb.html",
                           results=query_result,
                           team=team,
                           name=name,
                           reb=reb,
                           totalReb=total_reb)


@app.route('/average_stl')
def average_stl():
    query_string = "SELECT team_name, player_name, play, round(avg_stl::numeric,3), round((avg_stl*play)::numeric,0) FROM regular_season_stat_ranking ORDER BY avg_stl DESC LIMIT 15;"
    query_result = postgresql_query(query_string)
    team = []
    name = []
    stl = []
    total_stl = []
    for item in query_result:
        team.append(item[0])
        name.append(item[1])
        stl.append("%.3f" % float(item[3]))
        total_stl.append(int(item[4]))

    return render_template("average_stl.html",
                           results=query_result,
                           team=team,
                           name=name,
                           stl=stl,
                           totalStl=total_stl)


def postgresql_query(query_string: str, round=2):
    query_result = []
    cnn = pg.connect(database=cfg.database,
                     user=cfg.user,
                     password=cfg.password,
                     host=cfg.host,
                     port=cfg.port)
    cur = cnn.cursor()
    cur.execute(query_string)
    result_objs = cur.fetchall()
    for item in result_objs:
        query_result.append(item)
    cur.close()
    cnn.close()
    return result_objs


if __name__ == '__main__':
    app.run()