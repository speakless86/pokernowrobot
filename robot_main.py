#!/usr/bin/env python3
"""Robot main."""
import argparse
import logging

from pokernow_listener import start_listener


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

    start_listener(args.game_id[0], args.debug)
    # driver = webdriver.Chrome()
    # driver.get('https://www.pokernow.club/games/pgl8h8Tp4oQ7zRWjfWtwfHx74')
    # send_message(driver, 'Hello World!')
    # time.sleep(5)
    # driver.quit()


if __name__ == '__main__':
    main()
