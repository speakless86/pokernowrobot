#!/usr/bin/env python3
"""Listen Pokernow Game with SocketIO."""
import argparse
import json
import os
import logging
import sys

import socketio


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-gid',
        '--game-id',
        dest='game_id',
        help='pokernow.club game id',
        nargs=1,
        required=True)
    args = parser.parse_args()
    if not args.game_id:
        logging.error('You must specify a game id!')
        sys.exit()
    return args


def get_cookie():
    npt = os.getenv('POKERNOW_NPT')
    return f'npt={npt};'


def start_server(game_id, cookie):
    logging.info(f'args={game_id} cookie={cookie}')
    socket_client = socketio.Client()

    @socket_client.event
    def connect():
        logging.info('Connection has established.')

    @socket_client.event
    def connect_error(data):
        logging.warning(json.dumps(data, indent=4))

    @socket_client.event
    def message(data):
        logging.info(json.dumps(data, indent=4))

    @socket_client.event
    def disconnect():
        logging.info('disconnected from server')

    @socket_client.on('*')
    def catch_all(event, data):
        logging.info(event)
        logging.info(json.dumps(data, indent=4))

    url = f'https://www.pokernow.club/socket.io/?gameID={game_id}&firstConnection=true&EIO=3'
    logging.info(f'Connecting to {url}')

    socket_client.connect(
        url,
        wait=True,
        wait_timeout=60,
        transports='websocket',
        headers={
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'Upgrade',
            'Host': 'www.pokernow.club',
            'Origin': 'https://www.pokernow.club',
            'Pragma': 'no-cache',
            'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
            'Sec-WebSocket-Version': '13',
            'Upgrade': 'websocket',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Cookie': cookie})
    socket_client.wait()


def main():
    args = parse_args()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    start_server(args.game_id[0], get_cookie())


if __name__ == '__main__':
    main()
