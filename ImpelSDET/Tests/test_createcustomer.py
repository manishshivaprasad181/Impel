import os
import pytest
from faker import Faker
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Tests.Login import login
from Tests.Login_validator import validate_login


@pytest.fixture(scope="module")
def driver_setup(setup_and_teardown):
    driver = setup_and_teardown
    print(os.environ.get('VALID_EMAIL'), os.environ.get('VALID_PASSWORD'))
    login(driver, os.environ.get('VALID_EMAIL'), os.environ.get('VALID_PASSWORD'))
    navigate_to_add_customer_page(driver)
    yield driver
    driver.quit()


fake = Faker()


def fill_out_customer_form(driver, name, S3Folder):
    driver.execute_script("window.scrollTo(0, 0);")
    name_field = driver.find_element(By.ID, "name")
    S3Folder_field = driver.find_element(By.NAME, "s3_folder")
    name_field.clear()
    S3Folder_field.clear()
    name_field.send_keys(name)
    S3Folder_field.send_keys(S3Folder)


def click_save_customer_button(driver):
    driver.find_element(By.ID, "save-customer").click()


def validate_validation_message(driver, message):
    validation_message_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, f".//td[contains(normalize-space(), '{message}')]"))
    )
    assert validation_message_element is not None


def navigate_to_add_customer_page(driver):
    customers_dropdown = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Customers')]")))
    customers_dropdown.click()
    list_option = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'List')]")))
    list_option_link = list_option.get_attribute('href')
    driver.get(list_option_link)
    WebDriverWait(driver, 10).until(EC.url_contains("/my-customer/"))
    add_customer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Add Customer')]")))
    add_customer_page = add_customer_button.get_attribute('href')
    driver.get(add_customer_page)


@pytest.mark.parametrize("name, S3Folder",
                         [("", ""),
                          (fake.company(), ""),
                          ("", fake.name()),
                          (fake.company(), fake.name())])
def test_empty_inputs(driver_setup, name, S3Folder):
    driver = driver_setup
    fill_out_customer_form(driver, name, S3Folder)
    click_save_customer_button(driver)
    if name == "":
        validate_validation_message(driver, "Name is required.")
        # If name is empty, check for validation message for name field
    if S3Folder == "":
        # If S3Folder is empty, check for validation message for S3 folder field
        validate_validation_message(driver, "S3 folder is required.")
    if ' ' in S3Folder:
        validate_validation_message(driver, "S3 folder cannot have spaces")


@pytest.mark.parametrize("name, S3Folder",
                         [("ABC Hyundai", "abchyundai")])
def test_alreadyaddedcustomer(driver_setup, name, S3Folder):
    driver = driver_setup
    fill_out_customer_form(driver, name, S3Folder)
    click_save_customer_button(driver)
    validation_message_element1 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, ".//td[contains(normalize-space(), 'Name is already in use.')]"))
    )
    # If S3Folder is empty, check for validation message for S3 folder field
    validation_message_element2 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, ".//td[contains(normalize-space(), 'S3 folder is already in "
                                                    "use.')]"))
    )
    validation_message_element3 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, ".//td[contains(normalize-space(), 'Email is already in use.')]")))

    assert validation_message_element1 or validation_message_element2 or validation_message_element3


@pytest.mark.parametrize("name, S3Folder",
                         [(fake.company(), fake.name().replace(' ', ''))])
def test_add_customer(driver_setup, name, S3Folder):
    driver = driver_setup
    fill_out_customer_form(driver, name, S3Folder)
    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.NAME, "password")
    email = email_input.get_attribute("value")
    password = password_input.get_attribute("value")
    click_save_customer_button(driver)
    WebDriverWait(driver, 20).until(EC.url_changes(driver.current_url))
    driver.get(driver.current_url)
    dropdown_menu = driver.find_element(By.ID, "navbar-login-menu")
    ActionChains(driver).move_to_element(dropdown_menu).click().perform()
    logout_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[text()='Log out']")))
    logout_link.click()
    driver.get(driver.current_url)
    logout_link = validate_login(driver, email, password)
    assert logout_link.is_displayed()
