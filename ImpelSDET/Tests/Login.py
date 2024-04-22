from selenium.webdriver.common.by import By


def login(driver, email, password):
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    email_field.clear()
    password_field.clear()
    email_field.send_keys(email)
    password_field.send_keys(password)
    driver.find_element(By.ID, "submit").click()