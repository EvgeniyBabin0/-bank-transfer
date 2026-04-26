from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:8000/?balance=30000&reserved=20001"


def open_transfer_form(driver):
    driver.get(BASE_URL)
    driver.find_element(
        By.XPATH,
        "//h2[normalize-space()='Рубли']/ancestor::div[1]"
    ).click()


def get_card_input(driver):
    return driver.find_element(
        By.XPATH,
        "//input[@placeholder='0000 0000 0000 0000']"
    )


def wait_for_amount_input(driver, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='1000']")
        )
    )


def find_amount_inputs(driver):
    return driver.find_elements(
        By.XPATH,
        "//input[@placeholder='1000']"
    )


def find_transfer_button(driver):
    return driver.find_elements(
        By.XPATH,
        "//span[normalize-space()='Перевести']"
    )


def test_card_number_17_digits_not_allowed(driver):
    open_transfer_form(driver)

    card_input = get_card_input(driver)
    card_input.clear()
    card_input.send_keys("11112222333344445")

    amount_fields = find_amount_inputs(driver)

    assert len(amount_fields) == 0, "Поле 'Сумма перевода' появилось при номере карты из 17 цифр"


def test_negative_amount_not_allowed(driver):
    open_transfer_form(driver)

    card_input = get_card_input(driver)
    card_input.clear()
    card_input.send_keys("1111222233334444")

    amount_input = wait_for_amount_input(driver)
    amount_input.clear()
    amount_input.send_keys("-1000")

    transfer_buttons = find_transfer_button(driver)

    assert len(transfer_buttons) == 0, "Кнопка 'Перевести' доступна при отрицательной сумме"