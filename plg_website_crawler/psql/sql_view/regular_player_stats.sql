-- View: public.regular_player_stats

-- DROP VIEW public.regular_player_stats;

CREATE OR REPLACE VIEW public.regular_player_stats
 AS
 SELECT player_stats.name AS player_name,
    team.name_tw AS team_name,
    count(*) AS play,
    sum(player_stats.duration) AS duration,
    sum(player_stats.pts) AS pts,
    sum(player_stats.twoptsmade) AS twoptsmade,
    sum(player_stats.twoptsshot) AS twoptsshot,
    sum(player_stats.threeptsmade) AS threeptsmade,
    sum(player_stats.threeptsshot) AS threeptsshot,
    sum(player_stats.ftmade) AS ftmade,
    sum(player_stats.ftshot) AS ftshot,
    sum(player_stats.reb) AS reb,
    sum(player_stats.oreb) AS oreb,
    sum(player_stats.dreb) AS dreb,
    sum(player_stats.ast) AS ast,
    sum(player_stats.stl) AS stl,
    sum(player_stats.blk) AS blk,
    sum(player_stats.tov) AS tov,
    sum(player_stats.foul) AS pf
   FROM player_stats,
    game_summary gs,
    team
  WHERE ((gs.game_id = player_stats.game_id) AND (gs.game_type = 2) AND (team.team_id = player_stats.team_id) AND (team.team_id = gs.team_id))
  GROUP BY team.name_tw, player_stats.name;
