-- Table: public.gym_info

-- DROP TABLE public.gym_info;

CREATE TABLE public.gym_info
(
    gym_id integer NOT NULL,
    gym_name text COLLATE pg_catalog."default",
    hometeam_id integer,
    CONSTRAINT gym_info_pkey PRIMARY KEY (gym_id)
)

TABLESPACE pg_default;