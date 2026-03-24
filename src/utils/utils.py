# -*- coding: utf-8 -*-
import os, sys, time, json, copy, logging
import re, collections, operator, random, math
import statistics, pathlib

# from dotenv import load_dotenv
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta, timezone
from typing import Callable, Iterator, Tuple, Any, Dict, List, Optional

MODULE_NAME = __name__.upper()

TZ_UTC_0 = timezone(timedelta(hours=0))
TZ_UTC_8 = timezone(timedelta(hours=8))

INFO_BLANK = ' ' * 40
WARNING_BLANK = ' ' * 43
ERROR_BLANK = ' ' * 41

SHORT_FORMAT = '%Y-%m-%d'
LONG_FORMAT = '%Y-%m-%d %H:%M:%S'
LONG_T_FORMAT = '%Y-%m-%dT%H:%M:%S'