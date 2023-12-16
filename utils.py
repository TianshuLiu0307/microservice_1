"""Support methods for application"""
import json
import os.path
import uuid
from typing import Dict
import cProfile
import pstats

import time
from jsonschema import validate, ValidationError


def transform_body_metrics_upload_data(payload: Dict) -> Dict or None:
    data = payload['data']
    return data


def get_root_path():
    return __file__.split('/utils.py', maxsplit=1)[0]


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time:.6f} seconds")

        return result

    return wrapper
