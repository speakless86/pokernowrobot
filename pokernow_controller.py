#!/usr/bin/env python3
"""Control Pokernow Game UI with Webdriver."""
import logging
import time


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


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


if __name__ == '__main__':
    main()
