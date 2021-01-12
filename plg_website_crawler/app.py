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
    query_string = "SELECT team_name, player_name, round(avg_ast::numeric,3) FROM regular_season_stat_ranking ORDER BY avg_ast DESC LIMIT 10;"
    query_result = postgresql_query(query_string)
    return render_template("average_ast.html", results=query_result)


@app.route('/average_blk')
def average_blk():
    query_string = "SELECT team_name, player_name, round(avg_blk::numeric,3) FROM regular_season_stat_ranking ORDER BY avg_blk DESC LIMIT 10;"
    query_result = postgresql_query(query_string)
    return render_template("average_blk.html", results=query_result)


@app.route('/average_pts')
def average_pts():
    query_string = "SELECT team_name, player_name, round(avg_pts::numeric,3) FROM regular_season_stat_ranking ORDER BY avg_pts DESC LIMIT 10;"
    query_result = postgresql_query(query_string)


    return render_template("average_pts.html", results=query_result)


@app.route('/average_reb')
def average_reb():
    query_string = "SELECT team_name, player_name, round(avg_reb::numeric,3) FROM regular_season_stat_ranking ORDER BY avg_reb DESC LIMIT 10;"
    query_result = postgresql_query(query_string)
    return render_template("average_reb.html", results=query_result)

@app.route('/average_stl')
def average_stl():
    query_string = "SELECT team_name, player_name, round(avg_stl::numeric,3) FROM regular_season_stat_ranking ORDER BY avg_stl DESC LIMIT 10;"
    query_result = postgresql_query(query_string)
    return render_template("average_stl.html", results=query_result)


def postgresql_query(query_string:str, round=2):
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
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run()