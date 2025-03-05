-- Create the 'company' table
CREATE TABLE IF NOT EXISTS company (
    id SERIAL PRIMARY KEY,
    current_ticker VARCHAR(10),
    cik INTEGER NOT NULL,                  -- CIK, central index key
    included_date DATE,                    -- date of inclusion in S&P 500 if known
    removed_date DATE,                     -- date of removal from S&P 500 if applicable
    current_name VARCHAR(255)              -- current name of he company if known
);

-- Create the 'ticker' table
CREATE TABLE IF NOT EXISTS ticker (
    id SERIAL PRIMARY KEY,                        -- 'id' will be auto-incremented
    company_id INTEGER REFERENCES company(id),   -- 'company_id' is a foreign key into 'company'
    symbol VARCHAR(10),                           -- 'symbol' is a string (VARCHAR)
    start_date DATE,                              -- date when ticker was first assigned to company
    end_date DATE                                 -- last date when ticker was assigned to company
);


-- Create the 'fin_facts' table
CREATE TABLE IF NOT EXISTS fin_facts (
    id SERIAL PRIMARY KEY,
    year INTEGER,
    company_id INTEGER REFERENCES company(id),
    revenue NUMERIC(20, 2),
    income NUMERIC(20,2)
)