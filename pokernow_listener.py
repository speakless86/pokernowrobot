#!/usr/bin/env python3
"""Listen Pokernow Game with SocketIO."""
import argparse
import json
import os
import logging
import sys
from datetime import datetime

import requests
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


def send_message(game_id, message):
    formated_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    logging.info(formated_time)
    response = requests.post(
        'https://www.pokernow.club/new-chat-message/?gameID={game_id}',
        headers={
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.pokernow.club',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Cookie': get_cookie()},
        data={'message': message})
    logging.info(response.text)


def start_server(game_id):
    socket_client = socketio.Client(request_timeout=60,
                                    logger=True,
                                    engineio_logger=True)

    @socket_client.event
    def connect():
        logging.info('Connection has established.')

    @socket_client.event
    def connect_error(data):
        logging.warning(json.dumps(data, indent=4))

    @socket_client.event
    def disconnect():
        logging.info('disconnected from server')

    @socket_client.on('*')
    def catch_all(event, data):
        logging.info('Event=' + event)
        logging.info(json.dumps(data, indent=4))
        if event == 'newChatMessage':
            logging.info('Sending message')
            send_message(game_id, 'received')

    url = f'https://www.pokernow.club/socket.io/?gameID={game_id}&firstConnection=true&EIO=3&&pingTimeout=60'
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
            'Cookie': get_cookie()})
    socket_client.wait()


def main():
    args = parse_args()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    start_server(args.game_id[0])


if __name__ == '__main__':
    main()
