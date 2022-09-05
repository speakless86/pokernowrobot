#!/usr/bin/env python3
"""Control Pokernow Game UI with Webdriver."""
import logging
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def send_message(driver):
    chat_button = WebDriverWait(
        driver,
        10).until(
        lambda x: x.find_element(
            By.XPATH,
            '//html/body/div[1]/div/div[1]/div[7]/div/button[2]'))
    chat_button.click()
    input_box = WebDriverWait(
        driver,
        10).until(
        lambda x: x.find_element(
            By.XPATH,
            '//*[@id="canvas"]/div[1]/div[7]/form/input'))
    input_box.send_keys('Hello World')
    input_box.send_keys(Keys.ENTER)


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    driver = webdriver.Chrome()
    driver.get('https://www.pokernow.club/games/pgl8h8Tp4oQ7zRWjfWtwfHx74')
    send_message(driver)
    time.sleep(5)
    driver.quit()


if __name__ == '__main__':
    main()
