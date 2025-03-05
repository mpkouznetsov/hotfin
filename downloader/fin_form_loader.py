import datetime
import enum
import pathlib
from abc import ABC
from abc import abstractmethod


class FormType(enum.Enum):
    """Type of filing to download"""
    FORM_10K = "10-K"
    FORM_10Q = "10-Q"


class FinFormLoader(ABC):
    @abstractmethod
    def load(self,
             directory: pathlib.Path,
             cik: str,
             start_date: datetime.date,
             form_type: FormType):
        pass


