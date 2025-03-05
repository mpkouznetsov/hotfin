"""
This will eventually iterate over available
submission files for each company
and load corresponding facts.
For now, this is a stub
"""
import json
import logging
import pathlib
import sys

from pandas.io.formats.format import return_docstring

from downloader.fin_form_loader import FormType
from downloader import download
from data_tier import fin_facts, sql_runner


def load_cik(data_dir: pathlib.Path, cik: int, form:FormType=FormType.FORM_10K):
    directory = data_dir / str(cik) / form.value
    logging.debug(f"loading financial data from {directory}")
    filings = [file for file in directory.iterdir()]
    for f in filings:
        name = f.with_suffix("").stem
        year = name.split('-')[1]
        # TODO extract financial data from the filing
        annual_data = fin_facts.FinData(
            year=year,
            cik=cik,
            revenue=10000.0,
            income=1000.0
        )
        fin_facts.add_fin_data(annual_data)


def load_everything(staging_dir: str):
    data_dir = pathlib.Path(staging_dir)

    company_tickers_path = data_dir / "company_tickers.json"
    with company_tickers_path.open("r") as f:
        company_tickers_dict = json.load(fp=f)

    ciks_with_filings = {
        int(file.name) for file in data_dir.iterdir()
        if file.is_dir()
    }
    logging.debug(f"ciks_with_filings={ciks_with_filings}")
    ciks_with_known_tickers = {v["cik_str"] for v in company_tickers_dict.values()}

    # for now only load ones we have tickers for in company_tickers_dict
    # TODO add companies whose tickers we got from other sources
    ciks = ciks_with_known_tickers & ciks_with_filings
    logging.debug(f"ciks={ciks}")

    companies = [
        {
            "current_name": v["title"],
            "current_ticker": v["ticker"],
            "cik": v["cik_str"],
        } for v in company_tickers_dict.values()
        if v["cik_str"] in ciks
    ]
    fin_facts.add_companies(companies)

    # TODO reflect ticker changes over time
    # For now we just assign current tickers to companies
    sql_runner.run_sql_file("sql/populate_ticker.sql")

    # Create staging table(s)
    sql_runner.run_sql_file("sql/create_staging.sql")

    logging.debug("Loading (fake) data for each CIK")
    for cik in ciks:
        load_cik(data_dir, cik)

    sql_runner.run_sql_file("sql/ingest_from_staging.sql")
    sql_runner.run_sql_file("sql/drop_staging.sql")


if __name__ == "__main__":
    download.setup_logging()

    if len(sys.argv) < 2:
        logging.error(f"usage: {__file__} staging_dir")
        exit(1)
    load_everything(sys.argv[1])