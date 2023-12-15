
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from pydantic import BaseModel
from strictyaml import YAML, load

import IoTAnalytics

# Project Directories
PACKAGE_ROOT = Path(IoTAnalytics.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "Database"
PROCESS_DIR = PACKAGE_ROOT / "Process"


class AppConfig(BaseModel):
    """
    Application-level config.
    """
    package_name: str
    Raw_Dynamo_Table: str
    Aggregate_Dynamo_Table: str
    Anomaly_Dynamo_Table: str
    Anomaly_Time_Check_Interval: int
    Resource:str
    HS_ALARM_MIN: int
    HS_ALARM_MAX: int
    OS_ALARM_MIN: int
    OS_ALARM_MAX: int
    TEMP_ALARM_MIN: int
    TEMP_ALARM_MAX: int
    StartTime: str
    EndTime:   str
    deviceid1: str
    deviceid2: str
    WaitTime: int

class Config(BaseModel):
    """Master config object."""
    app_config: AppConfig


def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Optional[Path] = None) -> YAML:
    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()
