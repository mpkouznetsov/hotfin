import pathlib
from datetime import datetime

import secedgar

from downloader import config, fin_form_loader


FORM_TYPE_2_FILING_TYPE = {
    fin_form_loader.FormType.FORM_10K: secedgar.FilingType.FILING_10K,
    fin_form_loader.FormType.FORM_10Q: secedgar.FilingType.FILING_10Q,
}

class SEFinFormLoader(fin_form_loader.FinFormLoader):
    def load(self,
             directory,
             cik: str,
             start_date: datetime.date,
             form_type: fin_form_loader.FormType):
        filing_type = FORM_TYPE_2_FILING_TYPE[form_type]
        ticker_filings = secedgar.filings(cik_lookup=cik,
                                          start_date=start_date,
                                          filing_type=filing_type,
                                          user_agent=config.config.downloader.user_agent)

        ticker_filings.save(directory)

