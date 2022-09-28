from unittest.mock import ANY

from behave import *
from selenium.common import exceptions
from selenium.webdriver.common.by import By

# The Selenium API could be better in its interface so add a bit of
# plumbing here to help us design sane, reusable steps

"""
Find a label containing LABEL on the page
"""


def find_label(context, label):
    return context.browser.find_element(
        By.XPATH, '//label[contains(.,"{}")]'.format(label)
    )


"""
Find a label matching LABEL on the page, click to focus its input
and send the VALUE down into the field.
"""


def fill_input_with_label(context, label, value):
    label = find_label(context, label).click()

    context.browser.switch_to.active_element.send_keys(value)


"""
Find a fieldset whose legend matches LEGEND and find the first label
within containing VALUE in its text.
"""


def find_option_with_label(context, legend, value):
    return context.browser.find_element(
        By.XPATH,
        '//fieldset/legend[contains(., "{}")]/..//label[contains(., "{}")]'.format(
            legend, value
        ),
    )


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
    fill_input_with_label(context, label, value)


@when('je coche la case "{}"')
def step_impl(context, label):
    find_label(context, label).click()


@when('je choisis "{}" pour "{}"')
def step_impl(context, value, legend):
    find_option_with_label(context, legend, value).click()


@when('je sélectionne "{}" pour "{}"')
def step_impl(context, options_list, legend):
    options = options_list.split(", ")

    for option in options:
        find_option_with_label(context, legend, option).click()


@when('je clique sur "{}"')
def step_impl(context, label):
    context.browser.find_element(By.LINK_TEXT, label).click()


@when("je soumets le formulaire")
def step_impl(context):
    context.browser.find_element(By.XPATH, '//form//*[@type="submit"]').click()


@then('un email a été envoyé à "{}"')
def step_impl(context, email):
    context.mocks["sib"].assert_called_with(email, payload=ANY)
