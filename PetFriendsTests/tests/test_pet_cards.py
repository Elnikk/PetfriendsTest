import pytest
from selenium.webdriver.common.by import By
import time


def test_all_pets_have_photos_names_ages(browser):
    browser.implicitly_wait(10)

    browser.get(browser.base_url)
    time.sleep(2)

    try:
        show_all_pets_button = browser.find_element("id", "show_all_pets")
        show_all_pets_button.click()
        time.sleep(1)
    except:
        pass

    cards = browser.find_elements(By.CLASS_NAME, "card")

    if not cards:
        cards = browser.find_elements(By.CSS_SELECTOR, ".card")

    assert len(cards) >= 3

    for i, card in enumerate(cards):
        images = card.find_elements(By.TAG_NAME, "img")
        assert len(images) > 0

        img = images[0]
        src = img.get_attribute('src')
        assert src and src != ''
        assert img.is_displayed()

        name_element = card.find_element(By.CLASS_NAME, "card-title")
        name = name_element.text.strip()
        assert name != ''
        assert len(name) >= 2

        description_element = card.find_element(By.CLASS_NAME, "card-text")
        description = description_element.text.strip()
        assert description != ''

        has_digits = any(char.isdigit() for char in description)
        assert has_digits

        text_without_digits = ''.join([c for c in description if not c.isdigit()]).strip()
        assert len(text_without_digits) > 0


def test_implicit_wait_effectiveness(browser):
    browser.implicitly_wait(0.5)
    browser.get(browser.base_url)

    try:
        elements = browser.find_elements(By.CLASS_NAME, "card")
    except:
        pass

    browser.implicitly_wait(10)
    browser.refresh()

    elements = browser.find_elements(By.CLASS_NAME, "card")

    browser.implicitly_wait(10)

    assert len(elements) > 0