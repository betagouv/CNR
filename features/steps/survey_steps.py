from behave import *
from selenium.webdriver.common.by import By


@when("je remplis toutes les questions du formulaire")
def step_impl(context):
    inputs = context.browser.find_elements(By.XPATH, '//form//*[@type="text"]')

    for input in inputs:
        input.send_keys("foobar")
