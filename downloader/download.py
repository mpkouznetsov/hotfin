import datetime
import json
import logging
import pathlib
from typing import List, Dict

from secedgar import exceptions

from downloader import (
     components, company_tickers, config, fin_form_loader, sec_edgar_loader
)

DATE_FORMAT = "%Y-%m-%d"

logger = logging.getLogger(__name__)
loader = sec_edgar_loader.SEFinFormLoader()


def download_forms(
        directory: pathlib.Path,
        ciks: List[int],
        form_type=fin_form_loader.FormType.FORM_10K
) -> Dict[str,List[int]]:
    logging.debug("download_forms")

    result = {
        "successes": [],
        "failures": [],
    }
    start_date = config.config.downloader.history_start_date
    for t in ciks:
        logging.debug(f"Loading cik {t}")
        try:
            loader.load(
                directory,
                str(t),
                start_date,
                form_type=form_type,
            )
            result["successes"].append(t)
        except exceptions.NoFilingsError as e:
            logging.error(f"Failed to load filings for {t}", e)
            # just skip it
            result["errors"].append(t)
    return result


def setup_logging():
    log_file = pathlib.Path.home() / config.config.logging.file  # Ensure log file is in the home directory
    logging.basicConfig(
        level=getattr(logging, config.config.logging.level),  # Convert string to logging level
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # Log to a file
            logging.StreamHandler()         # Also log to console
        ]
    )


def download():
    root_dir = pathlib.Path(config.config.downloader.data_dir)
    today = datetime.date.today()
    today_str = today.strftime(DATE_FORMAT)
    session_dir = root_dir / today_str
    session_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Initiating download to {session_dir}")

    # Load CIK-ticker-title mapping
    cik_ticker_title = company_tickers.download_company_tickers(session_dir)

    # get tickers to load
    as_of_date = config.config.downloader.sp500_composition_date
    tickers_as_of = components.load_components(as_of_date)
    logging.info(
        f"As of {as_of_date} date there were {len(tickers_as_of)} components."
    )

    today_components = components.download_current(session_dir)

    # all companies currently in S&P 500 that have been there
    # since at least the as_of_date
    ciks_still_there = [
        c.cik for c in today_components
        if c.date_added <= as_of_date
    ]
    # TODO: there is a possibility that a ticker _today_ is attributed
    # to a different company than on as_of_date.
    ciks_found = [
        ctt['cik_str'] for ctt in cik_ticker_title.values()
        if ctt['ticker'] in today_components
    ]
    ciks = list(set(ciks_still_there + ciks_found))
    logging.info(f"Loading {len(ciks)} histories")
    logging.debug(",".join([str(x) for x in ciks]))

    res = download_forms(session_dir, ciks)

    result_path = session_dir / "result.json"
    with result_path.open("w", encoding="utf-8") as f:
        json.dump(res, f, indent=4)


if __name__ == "__main__":
    setup_logging()

    # TODO add command line argument for config file path

    download()