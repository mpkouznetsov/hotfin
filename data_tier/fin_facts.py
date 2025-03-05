import dataclasses
import logging
from typing import List, Dict, Any

import psycopg2

from downloader import config


@dataclasses.dataclass
class FinData:
    year: int
    cik: int
    revenue: float
    income: float


def get_config():
    db_config = config.config.database
    return {
        "dbname": "postgres",
        "user": db_config.user,
        "password": db_config.password,
        "host": db_config.host,
    }


def add_fin_data(annual_data: FinData):
    table_name = "fin_facts_staging"
    columns = ["cik", "revenue", "income", "year"]
    data = [{
        "cik": annual_data.cik,
        "revenue": annual_data.revenue,
        "income": annual_data.income,
        "year": annual_data.year,
    }]
    _insert_data(table_name, columns, data)


def add_companies(company_list: List[Dict[str,Any]]):
    table_name = "company"
    columns = ["current_name", "current_ticker", "cik"]
    _insert_data(table_name, columns, company_list)


def _insert_data(
        table_name: str,
        columns: List[str],
        data: List[Dict[str,Any]]
):
    insert_query = f"""
    INSERT INTO {table_name} ({', '.join(columns)})
    VALUES ({', '.join(['%s'] * len(columns))})
    """
    try:
        # Establish connection
        with psycopg2.connect(**get_config()) as conn:
            with conn.cursor() as cur:
                # Convert list of dictionaries to list of tuples
                values = [tuple(d[col] for col in columns) for d in data]

                # Execute batch insert
                cur.executemany(insert_query, values)
        logging.debug("Data inserted successfully!")
    except psycopg2.Error as e:
        logging.error(f"Error inserting data", e)
        raise e
