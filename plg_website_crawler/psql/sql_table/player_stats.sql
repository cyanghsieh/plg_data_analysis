-- Table: public.player_stats

-- DROP TABLE public.player_stats;

CREATE TABLE public.player_stats
(
    game_id integer,
    team_id integer,
    jersey_number integer,
    start_lineup boolean,
    name text COLLATE pg_catalog."default",
    duration double precision,
    twoptsmade double precision,
    twoptsshot double precision,
    twoptspct double precision,
    threeptsmade double precision,
    threeptsshot double precision,
    threeptspct double precision,
    ftmade double precision,
    ftshot double precision,
    ftpct double precision,
    pts double precision,
    reb double precision,
    oreb double precision,
    dreb double precision,
    ast double precision,
    stl double precision,
    blk double precision,
    tov double precision,
    foul double precision,
    eff double precision,
    ud double precision,
    tspct double precision,
    usgpct double precision,
    efgpct double precision
)

TABLESPACE pg_default;