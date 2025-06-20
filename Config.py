import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class Config:
    show_logs: bool = False
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            show_logs = os.getenv("SHOW_LANGCHAIN_LOGS",
                                  "false").lower() == "true"
            cls._instance = super().__new__(cls)
            cls._instance.show_logs = show_logs
        return cls._instance
