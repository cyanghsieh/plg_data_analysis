-- View: public.regular_season_stat_ranking

-- DROP VIEW public.regular_season_stat_ranking;

CREATE OR REPLACE VIEW public.regular_season_stat_ranking
 AS
 SELECT regular_player_stats.team_name,
    regular_player_stats.player_name,
    regular_player_stats.play,
    (regular_player_stats.pts / (regular_player_stats.play)::double precision) AS avg_pts,
    (regular_player_stats.reb / (regular_player_stats.play)::double precision) AS avg_reb,
    (regular_player_stats.stl / (regular_player_stats.play)::double precision) AS avg_stl,
    (regular_player_stats.blk / (regular_player_stats.play)::double precision) AS avg_blk,
    (regular_player_stats.ast / (regular_player_stats.play)::double precision) AS avg_ast,
    (regular_player_stats.duration / (regular_player_stats.play)::double precision) AS avg_duration,
    (regular_player_stats.twoptsmade / NULLIF(regular_player_stats.twoptsshot, (0)::double precision)) AS avg_2pt,
    (regular_player_stats.threeptsmade / NULLIF(regular_player_stats.threeptsshot, (0)::double precision)) AS avg_3pt,
    (regular_player_stats.ftmade / NULLIF(regular_player_stats.ftshot, (0)::double precision)) AS avg_ft,
    (regular_player_stats.oreb / (regular_player_stats.play)::double precision) AS avg_oreb,
    (regular_player_stats.dreb / (regular_player_stats.play)::double precision) AS avg_dreb,
    (regular_player_stats.tov / (regular_player_stats.play)::double precision) AS avg_turnover,
    (regular_player_stats.pf / (regular_player_stats.play)::double precision) AS avg_pf
   FROM regular_player_stats
  WHERE (regular_player_stats.duration > (0)::double precision);