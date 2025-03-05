INSERT INTO fin_facts (year, company_id, revenue, income)
SELECT
    ffs.year,
    c.id AS company_id,
    ffs.revenue,
    ffs.income
FROM fin_facts_staging ffs
JOIN company c ON ffs.cik = c.cik;