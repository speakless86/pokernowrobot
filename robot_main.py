#!/usr/bin/env python3
"""Robot main."""
import argparse
import os
import time
import logging
import json

from selenium import webdriver

from pokernow_listener import start_listener
from pokernow_controller import send_message

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-gid',
        '--game-id',
        dest='game_id',
        help='pokernow.club game id',
        nargs=1,
        required=True)
    parser.add_argument(
        '--debug',
        dest='debug',
        help='debug mode',
        nargs='?',
        default=False,
        type=bool)
    args = parser.parse_args()
    if not args.game_id:
        logging.error('You must specify a game id!')
        sys.exit()
    return args


def main():
    args = parse_args()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    url = f'https://www.pokernow.club/games/{args.game_id[0]}'
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait for manual login
    logging.info('Enter into sleep for 30 seconds.')
    time.sleep(30)
    logging.info('Exit from sleeping.')

    cookie_list = driver.get_cookies()
    apt_cookie = ''
    npt_cookie = ''
    for cookie in cookie_list:
        if cookie['name'] == 'apt':
            apt_cookie=cookie['value']
        if cookie['name'] == 'npt':
            npt_cookie=cookie['value']

    # send_message(driver, 'Hello World!')
    start_listener(args.game_id[0], args.debug, apt_cookie, npt_cookie)


if __name__ == '__main__':
    main()
