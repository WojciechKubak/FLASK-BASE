from flask import Flask, request_started, request
from typing import Any
import logging

logging.basicConfig(level=logging.INFO)


def log_request_started(sender: Flask, **extras: dict[str, Any]) -> None:
    logging.info('Request started')
    logging.info(f'{sender=}')
    logging.info(f'{extras=}')
    logging.info(f"URL: {request.url}")
    logging.info(f"Method: {request.method}")
    logging.info(f"Headers: {request.headers}")


request_started.connect(log_request_started)
