#!/usr/bin/env python3
"""Control Pokernow Game UI with Webdriver."""
import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def create_driver(game_id):
    url = f'https://www.pokernow.club/games/{game_id}'
    driver = webdriver.Chrome()
    driver.get(url)

    logging.info('Please sign in your PokerNow account in Chrome.')
    _ = input('Press any key to continue.')
    return driver


def get_cookie_value_by_name(driver, cookie_name):
    cookie_list = driver.get_cookies()
    for cookie in cookie_list:
        if cookie['name'] == cookie_name:
            return cookie['value']


def send_message(driver, message):
    chat_button = WebDriverWait(
        driver,
        2).until(
        lambda x: x.find_element(
            By.XPATH,
            '//html/body/div[1]/div/div[1]/div[7]/div/button[2]'))
    chat_button.click()
    input_box = WebDriverWait(
        driver,
        2).until(
        lambda x: x.find_element(
            By.XPATH,
            '//*[@id="canvas"]/div[1]/div[7]/form/input'))
    input_box.send_keys(message)
    input_box.send_keys(Keys.ENTER)


def fold(driver):
    fold_button = WebDriverWait(
        driver,
        2).until(
        lambda x: x.find_element(
            By.XPATH,
            '//*[@id="canvas"]/div[1]/div/div[7]/div/button[contains(@class, "fold")]'))
    fold_button.click()


def check_or_call(driver):
    try:
        check_button = WebDriverWait(
            driver,
            2).until(
            lambda x: x.find_element(
                By.XPATH,
                '//*[@id="canvas"]/div[1]/div/div[7]/div/button[contains(@class, "check")]'))
        check_button.click()
    except NoSuchElementException:
        call(driver)

def call(driver):
    call_button = WebDriverWait(
        driver,
        2).until(
        lambda x: x.find_element(
            By.XPATH,
            '//*[@id="canvas"]/div[1]/div/div[7]/div/button[contains(@class, "call")]'))
    call_button.click()

def bet(driver, amount, dry_run=False):
    logging.info(f'Hero is going to open {amount}. (dry_run={dry_run})')

    if dry_run:
        return

    bet_button = WebDriverWait(
        driver,
        5).until(
        lambda x: x.find_element(
            By.XPATH,
            '//*[@id="canvas"]/div[1]/div/div[7]/div/button[contains(@class, "raise")]'))
    bet_button.click()

    input_box = WebDriverWait(
        driver,
        5).until(
        lambda x: x.find_element(
            By.XPATH,
            '//*[@id="canvas"]/div[1]/div/div[7]/form/div[1]/div/input'))
    input_box.send_keys(int(amount))
    input_box.send_keys(Keys.ENTER)


if __name__ == '__main__':
    main()
