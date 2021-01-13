-- View: public.regular_game_summary

-- DROP VIEW public.regular_game_summary;

CREATE OR REPLACE VIEW public.regular_game_summary
 AS
 SELECT game_summary.game_id,
    game_summary.date,
    game_summary.game_type,
    game_summary.gym_id,
    game_summary.team_id,
    game_summary.home,
    game_summary.win,
    game_summary.q1,
    game_summary.q2,
    game_summary.q3,
    game_summary.q4,
    game_summary.ot1,
    game_summary.ot2,
    game_summary.ot3,
    game_summary.final
   FROM game_summary
  WHERE (game_summary.game_type = 2);

