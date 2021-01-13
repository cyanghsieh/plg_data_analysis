-- View: public.standings

-- DROP VIEW public.standings;

CREATE OR REPLACE VIEW public.standings
 AS
 SELECT team.name_tw AS "隊名",
    count(reg.*) AS "已賽",
    count(reg.*) FILTER (WHERE (reg.win = true)) AS "勝場",
    ((count(reg.*) FILTER (WHERE (reg.win = true)))::double precision / (count(reg.*))::double precision) AS "總勝率",
    count(reg.*) FILTER (WHERE ((reg.win = true) AND (reg.home = true))) AS "主場勝",
    count(reg.*) FILTER (WHERE (reg.home = true)) AS "主場戰",
    count(reg.*) FILTER (WHERE ((reg.win = true) AND (reg.home = false))) AS "客場勝",
    count(reg.*) FILTER (WHERE (reg.home = false)) AS "客場戰"
   FROM team,
    regular_game_summary reg
  WHERE (team.team_id = reg.team_id)
  GROUP BY team.team_id;

COMMENT ON VIEW public.standings
    IS '戰績表';

