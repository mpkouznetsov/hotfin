INSERT INTO ticker (company_id, symbol, start_date)
SELECT id, current_ticker, included_date
FROM company;
