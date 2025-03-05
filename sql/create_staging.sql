drop table if exists fin_facts_staging;

create table fin_facts_staging (
    cik INTEGER NOT NULL,
    revenue NUMERIC(20, 2),
    income NUMERIC(20, 2),
    year INTEGER
)