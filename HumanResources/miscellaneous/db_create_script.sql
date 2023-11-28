-- Table: public.employees

-- DROP TABLE IF EXISTS public.employees;

CREATE TABLE IF NOT EXISTS public.employees
(
    id bigint not null,
    first_name text COLLATE pg_catalog."default",
    last_name text COLLATE pg_catalog."default",
    email text COLLATE pg_catalog."default",
    gender text COLLATE pg_catalog."default",
    date_of_birth text COLLATE pg_catalog."default",
    industry text COLLATE pg_catalog."default",
    salary double precision,
    years_of_experience double precision
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.employees
    OWNER to postgres;