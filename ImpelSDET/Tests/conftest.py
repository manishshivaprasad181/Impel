import time

import pytest
from selenium import webdriver


@pytest.fixture(scope="module")
def setup_and_teardown():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://test-engineer-assignment-manager.testenv.impel.io/login?next=%2F")
    yield driver
    driver.quit()
