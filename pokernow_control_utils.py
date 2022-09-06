#!/usr/bin/env python3
"""Control Pokernow Game UI with Webdriver."""
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def create_driver_and_wait(game_id, wait_seconds):
    url = f'https://www.pokernow.club/games/{game_id}'
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait for manual login
    logging.info(f'Enter into sleep for {wait_seconds} seconds.')
    time.sleep(wait_seconds)
    logging.info('Exit from sleeping.')
    return driver


def get_cookie_value_by_name(driver, cookie_name):
    cookie_list = driver.get_cookies()
    for cookie in cookie_list:
        if cookie['name'] == cookie_name:
            return cookie['value']


def send_message(driver, message):
    chat_button = WebDriverWait(
        driver,
        5).until(
        lambda x: x.find_element(
            By.XPATH,
            '//html/body/div[1]/div/div[1]/div[7]/div/button[2]'))
    chat_button.click()
    input_box = WebDriverWait(
        driver,
        5).until(
        lambda x: x.find_element(
            By.XPATH,
            '//*[@id="canvas"]/div[1]/div[7]/form/input'))
    input_box.send_keys(message)
    input_box.send_keys(Keys.ENTER)


def fold(driver):
    logging.info('Folding')
    fold_button = WebDriverWait(
        driver,
        5).until(
        lambda x: x.find_element(
            By.XPATH,
            '//*[@id="canvas"]/div[1]/div[6]/div/button[4]'))
    fold_button.click()


if __name__ == '__main__':
    main()
