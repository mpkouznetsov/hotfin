import logging
import pathlib
from typing import Dict, Any

import requests

from downloader import config

COMPANY_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
LOCAL_FILENAME = "company_tickers.json"

logger = logging.getLogger(__name__)

def download_company_tickers(directory: pathlib.Path) -> Dict[str, Any]:
    """
    Load https://www.sec.gov/files/company_tickers.json
    The download directory must exist
    :param directory where the file is to be downloaded
    """
    user_agent = config.config.downloader.user_agent
    headers = {
        "User-Agent": user_agent,
    }
    assert directory.is_dir()
    file_path = directory / LOCAL_FILENAME

    response = requests.get(COMPANY_TICKERS_URL, headers=headers)
    if response.status_code == 200:
        with file_path.open("w", encoding="utf-8") as file:
            file.write(response.text)
            logging.debug(f"Downloaded {LOCAL_FILENAME}")
    else:
        logging.error(f"Failed to load {LOCAL_FILENAME}, status_code={response.status_code},"
                      f"Error message: \"{response.text}\"")
        response.raise_for_status()
    return response.json()

