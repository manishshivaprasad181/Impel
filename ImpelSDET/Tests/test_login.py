import os
import pytest
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Tests.Login import login
from Tests.Login_validator import validate_login

fake = Faker()


@pytest.mark.parametrize("email, password", [
    (fake.email(), fake.password()),
    (fake.email(), fake.password()),
    (fake.email(), fake.password())
])
def test_login_with_invalid_credentials(setup_and_teardown, email, password):
    driver = setup_and_teardown
    login(driver, email, password)
    invalid_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//li[text()='Invalid username or password']")))
    assert invalid_message.text == "Invalid username or password"


@pytest.mark.parametrize("email, password", [
    ("", fake.password()),
    (fake.email(), ""),
    ("", "")
])
def test_login_with_empty_credentials(setup_and_teardown, email, password):
    driver = setup_and_teardown
    login(driver, email, password)
    assert (driver.find_element(By.ID, "email").get_attribute("validationMessage") == "Please fill out this field." or
            driver.find_element(By.ID, "password").get_attribute("validationMessage") == "Please fill out this field.")


@pytest.mark.parametrize("email, password", [(os.environ.get('VALID_EMAIL'), os.environ.get('VALID_PASSWORD'))])
def test_login_with_valid_credentials(setup_and_teardown, email, password):
    driver = setup_and_teardown
    logout_link = validate_login(driver, email, password)
    assert logout_link.is_displayed()
