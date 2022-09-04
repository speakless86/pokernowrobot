#!/usr/bin/env python3

import argparse
import logging

import socketio


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-gid',
        '--game-id',
        dest="game_id",
        help='pokernow.club game id',
        nargs=1,
        required=True)
    parser.add_argument(
        '-n',
        '--npt',
        dest="npt",
        default='',
        help='pokernow.club npt cookie value (copy from browser)',
        nargs=1)
    parser.add_argument(
        '-a',
        '--apt',
        dest="apt",
        default='',
        help='pokernow.club apt cookie value (copy from browser)',
        nargs=1)
    args = parser.parse_args()
    if not args.game and (not args.npt or not args.apt):
        logging.error("You must a gameid and a npt/apt cookie value")
        exit()
    return args


def get_cookie(apt, npt):
    cookie_string = ''
    cookie_string += f'apt={apt};' if apt else ''
    cookie_string += f'npt={npt};' if npt else ''
    return cookie_string


def start_server(game_id, cookie):
    logging.info(f'args={args} cookie={cookie}')
    socket_client = socketio.Client()


def main():
    args = parse_args()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    start_server(args.game_id, get_cookie(args.apt, args.npt))


if __name__ == '__main__':
    main()
