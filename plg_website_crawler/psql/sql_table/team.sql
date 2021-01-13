-- Table: public.team

-- DROP TABLE public.team;

CREATE TABLE public.team
(
    team_id integer NOT NULL,
    name_tw text COLLATE pg_catalog."default",
    CONSTRAINT team_pkey PRIMARY KEY (team_id)
)

TABLESPACE pg_default;