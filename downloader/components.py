"""
Determine S&P 500 constituents in the past.
Based on https://github.com/fja05680/sp500
(it is not directly reusable because it has all its code in notebooks)
"""

import io
from dataclasses import dataclass
from typing import List

import pandas as pd
import pathlib
import wikipedia as wp
from datetime import datetime


TITLE = 'List of S&P 500 companies'
CURRENT_FILENAME = "sp500.csv"
HISTORY_FILENAME = "immutable_data/sp500_history.csv"


@dataclass
class Component:
    ticker: str
    name: str
    date_added: datetime.date
    cik: int


def get_table(title, filename, match, use_cache=False):
    file = pathlib.Path(filename)
    if use_cache and file.is_file():
        pass
    else:
        html = wp.page(title).html()
        df = pd.read_html(io.StringIO(html), header=0, match=match)[0]
        df.to_csv(filename, header=True, index=False, encoding='utf-8')

    df = pd.read_csv(filename)
    return df


def download_current(directory: pathlib.Path) -> List[Component]:
    """
    Retrieve from https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
    Save the table as CSV
    :param directory where to save the file
    :return list of Component
    """
    file_path = directory / CURRENT_FILENAME
    df = get_table(TITLE, file_path, match='Symbol')
    df = df[['Symbol', 'Security', 'Date added', 'CIK']]
    df['Date added'] = pd.to_datetime(df['Date added']).dt.date
    return [Component(*row) for row in df.itertuples(index=False, name=None)]


def load_components(as_of: datetime.date) -> List[str]:
    """
    Load S&P 500 constituent companies' tickers as of a given date
    """
    df = pd.read_csv(HISTORY_FILENAME, index_col='date')

    # Get symbols on asof date
    as_of_str = as_of.strftime("%Y-%m-%d")
    df2 = df[df.index <= as_of_str]
    last_row = df2.tail(1)
    tickers = last_row['tickers'].iloc[0]
    return sorted(tickers.split(','))




