-- Table: public.game_summary

-- DROP TABLE public.game_summary;

CREATE TABLE public.game_summary
(
    game_id integer NOT NULL,
    date timestamp with time zone NOT NULL,
    game_type integer NOT NULL,
    gym_id integer NOT NULL,
    team_id integer NOT NULL,
    home boolean,
    win boolean,
    q1 smallint,
    q2 smallint,
    q3 smallint,
    q4 smallint,
    ot1 smallint,
    ot2 smallint,
    ot3 smallint,
    final smallint
)

TABLESPACE pg_default;