import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Tests.Login import login
from selenium.webdriver.support import expected_conditions as EC


def validate_login(driver, email, password):
    login(driver, email, password)
    time.sleep(1)
    WebDriverWait(driver, 10).until_not(
        EC.url_to_be("https://test-engineer-assignment-manager.testenv.impel.io/login?next=%2F"))
    driver.get(driver.current_url)
    dropdown_menu = driver.find_element(By.ID, "navbar-login-menu")
    ActionChains(driver).move_to_element(dropdown_menu).click().perform()
    logout_link = driver.find_element(By.XPATH, "//ul[@class='dropdown-menu']//a[text()='Log out']")
    return logout_link
