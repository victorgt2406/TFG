"Applications logs manager"
import json
from enum import Enum
from pydantic import BaseModel


class PrintlogConfigSchema(BaseModel):
    "log-congif.json schema"
    info: bool
    warning: bool
    error: bool


class PrintlogEnum(Enum):
    "LogType enum: INFO, WARNING, ERROR"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


def load_config() -> dict[str, bool]:
    "Loads the config file"
    with open("./printlog-config.json", "r", encoding="utf-8") as f:
        return json.load(f)


CONFIG: dict[str, bool] = {
    "info": True,
    "warning": True,
    "error": True
}
CONFIG = load_config()


def printlog(msg: str, log_type: PrintlogEnum) -> None:
    "Prints the log if it is allowed"
    if CONFIG[log_type.value]:
        print(f"{log_type.value.upper()}: {msg}")
