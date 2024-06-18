#!/usr/bin/env python

from decouple import config
from unipath import Path

BASE_DIR = Path(__file__).parent

LOG_LEVEL = config("LOG_LEVEL", cast=str, default="WARNING")
DEFAULT_TZ = config("TZ", cast=str, default="Europe/London")
