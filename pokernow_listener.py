#!/usr/bin/env python3
"""Listen Pokernow Game with SocketIO."""
import json
import os
import logging
import sys

import socketio

from pokernow_processor import PokerNowProcessor


def get_cookie(apt_cookie, npt_cookie):
    return f'npt={npt_cookie};apt={apt_cookie};'


def start_listener(game_id, debug, apt_cookie, npt_cookie):
    socket_client = socketio.Client(request_timeout=60,
                                    logger=debug,
                                    engineio_logger=debug)
    processer = PokerNowProcessor()

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
        processer.process(event, data)

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
            'Cookie': get_cookie(apt_cookie, npt_cookie)})
    socket_client.wait()
