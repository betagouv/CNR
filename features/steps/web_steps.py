from behave import *
from selenium.webdriver.common.by import By

def get_input_for_label(context, label):
    return context.browser.find_element(By.XPATH, "//label[contains(.,'{}')]//following::input[1]".format(label))

@when("je me rends sur la page d'accueil")
def step_impl(context):
    context.browser.get(context.get_url("/"))

@then('je peux lire "{}" dans la page')
def step_impl(context, text):
    assert text in context.browser.find_element(By.TAG_NAME, "main").text

@then('la page est titrée "{}"')
def step_impl(context, title):
    assert context.browser.title == title

@when('je remplis le champ "{}" avec "{}"')
def step_impl(context, label, value):
    get_input_for_label(context, label).send_keys(value)

@when('je coche la case "{}"')
def step_impl(context, label):
    get_input_for_label(context, label).click()

@when('je clique sur "{}"')
def step_impl(context, label):
    context.browser.find_element(By.LINK_TEXT, label).click()
