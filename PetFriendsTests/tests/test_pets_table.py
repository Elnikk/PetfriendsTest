import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_my_pets_table_with_explicit_waits(auth_browser):
    browser = auth_browser

    wait = WebDriverWait(browser, 10)

    title = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert "Мои питомцы" in title.text

    alert = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-info"))
    )
    assert "питомца" in alert.text or "питомцев" in alert.text

    table = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
    assert table.is_displayed()

    rows = wait.until(
        lambda driver: driver.find_elements(By.CSS_SELECTOR, "tbody tr") and
                       len(driver.find_elements(By.CSS_SELECTOR, "tbody tr")) > 0
    )

    for i in range(len(rows)):
        row_num = i + 1

        try:
            photo = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//tbody/tr[{row_num}]/td[1]/img")
                )
            )
            src = photo.get_attribute('src')
            assert src and src != ''
            assert photo.is_displayed()
        except:
            pass

        name = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//tbody/tr[{row_num}]/td[2]")
            )
        )
        name_text = name.text.strip()
        assert name_text != ''

        breed = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//tbody/tr[{row_num}]/td[3]")
            )
        )
        breed_text = breed.text.strip()
        assert breed_text != ''

        age = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//tbody/tr[{row_num}]/td[4]")
            )
        )
        age_text = age.text.strip()
        assert age_text != ''

        has_digits = any(char.isdigit() for char in age_text)
        assert has_digits


def test_different_explicit_conditions(auth_browser):
    browser = auth_browser

    wait = WebDriverWait(browser, 10)

    button = wait.until(
        EC.element_to_be_clickable((By.ID, "show_all_pets"))
    )
    assert button.is_enabled() and button.is_displayed()

    wait.until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "tbody"), "Барсик")
    )

    table = browser.find_element(By.TAG_NAME, "table")
    visible_table = wait.until(
        EC.visibility_of(table)
    )
    assert visible_table.is_displayed()

    try:
        wait.until(
            EC.invisibility_of_element_located((By.ID, "non_existent_element"))
        )
    except:
        pass

    rows_before = browser.find_elements(By.CSS_SELECTOR, "tbody tr")
    if len(rows_before) > 0:
        first_row = rows_before[0]

        browser.execute_script("arguments[0].remove();", first_row)

        wait.until(
            EC.staleness_of(first_row)
        )