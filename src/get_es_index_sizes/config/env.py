#!/usr/bin/env python

import os

from decouple import config
from unipath import Path

BASE_DIR = Path(__file__).parent

LOG_LEVEL = config("LOG_LEVEL", cast=str, default="WARNING")
DEFAULT_TZ = config("TZ", cast=str, default="Europe/London")

OUTPUT_DIR = config("OUTPUT_DIR", cast=str, default=os.path.join(os.getcwd(), "output"))

ES_CLOUD_ID = config("ES_CLOUD_ID", cast=str, default=None)
ES_API_KEY = config("ES_API_KEY", cast=str, default=None)

ES_URL = config("ES_URL", cast=str, default=None)
ES_USER = config("ES_USER", cast=str, default=None)
ES_PASS = config("ES_PASS", cast=str, default=None)
