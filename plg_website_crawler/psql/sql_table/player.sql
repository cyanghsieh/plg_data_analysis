-- Table: public.player

-- DROP TABLE public.player;

CREATE TABLE public.player
(
    id bigint NOT NULL,
    name_tw text COLLATE pg_catalog."default",
    name_en text COLLATE pg_catalog."default",
    jersey_number integer,
    "position" text COLLATE pg_catalog."default",
    height double precision,
    weight double precision,
    dob date,
    "foreign" boolean,
    CONSTRAINT player_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;