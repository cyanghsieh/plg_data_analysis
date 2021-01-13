-- View: public.regular_game_final_board

-- DROP VIEW public.regular_game_final_board;

CREATE OR REPLACE VIEW public.regular_game_final_board
 AS
 SELECT a.game_id,
    a.date AS "日期",
    a.name_tw AS "勝隊",
    a.final AS "勝隊得分",
    (a.final - b.final) AS "勝分差",
    b.name_tw AS "負隊",
    b.final AS "負隊得分"
   FROM (( SELECT game_summary.game_id,
            game_summary.date,
            team.name_tw,
            game_summary.final
           FROM game_summary,
            team
          WHERE ((game_summary.game_type = 2) AND (team.team_id = game_summary.team_id) AND (game_summary.win = true))) a
     JOIN ( SELECT game_summary.game_id,
            team.name_tw,
            game_summary.final
           FROM game_summary,
            team
          WHERE ((game_summary.game_type = 2) AND (team.team_id = game_summary.team_id) AND (game_summary.win = false))) b ON ((a.game_id = b.game_id)));
