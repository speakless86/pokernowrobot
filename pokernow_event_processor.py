#!/usr/bin/env python3
"""Process Pokernow Events"""
import json
import logging


def process(event, data):
    logging.info('Event=' + event)
    logging.info(json.dumps(data, indent=4))
