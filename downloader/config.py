import datetime
import pathlib
import pydantic
import yaml
from pydantic import BaseModel, Field


class DatabaseConfig(pydantic.BaseModel):
    host: str
    port: int
    user: str
    password: str


class DownloaderConfig(pydantic.BaseModel):
    user_agent: str
    history_start_date: datetime.date
    sp500_composition_date: datetime.date
    data_dir: str


class LoggingConfig(BaseModel):
    level: str = Field(..., pattern="DEBUG|INFO|WARNING|ERROR|CRITICAL")
    file: str  # Log filename (e.g., "logs/app.log")


class AppConfig(BaseModel):
    database: DatabaseConfig
    downloader: DownloaderConfig
    logging: LoggingConfig


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        config_path = pathlib.Path.home() / "hotfin.yaml"
        with config_path.open("r") as file:
            raw_config = yaml.safe_load(file)

        try:
            self.data = AppConfig(**raw_config)  # Validate with Pydantic
        except pydantic.ValidationError as e:
            print("Configuration validation failed:", e)
            raise

    def get(self):
        return self.data  # Return the validated config object

# Create a global singleton instance
config = Config().get()
