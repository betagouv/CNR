from unittest.mock import ANY

from behave import then, when
from selenium.webdriver.common.by import By

# The Selenium API could be better in its interface so add a bit of
# plumbing here to help us design sane, reusable steps


def find_label(context, label):
    """
    Find a label containing LABEL on the page
    """
    return context.browser.find_element(
        By.XPATH, '//label[contains(.,"{}")]'.format(label)
    )


def find_checkbox_label(context, label):
    """
    Find a checkbox by its label on the page
    """
    return context.browser.find_element(
        By.XPATH, '//label[contains(.,"{}")]/span'.format(label)
    )


def fill_input_with_label(context, label, value):
    """
    Find a label matching LABEL on the page, click to focus its input
    and send the VALUE down into the field.
    """
    label = find_label(context, label).click()

    context.browser.switch_to.active_element.send_keys(value)


def find_option_with_label(context, legend, value):
    """
    Find a fieldset whose legend matches LEGEND and find the first label
    within containing VALUE in its text.
    """
    return context.browser.find_element(
        By.XPATH,
        '//fieldset/legend[contains(., "{}")]/..//label[contains(., "{}")]'.format(
            legend, value
        ),
    )


@when("je me rends sur la page d'accueil")
def step_go_to_homepage(context):
    context.browser.get(context.get_url("/"))


@then('je peux lire "{}" dans la page')
def step_read_page_contains(context, text):
    assert text in context.browser.find_element(By.TAG_NAME, "main").text


@then('la page est titrée "{}"')
def step_read_page_title(context, title):
    assert context.browser.title == title


@when('je remplis le champ "{}" avec "{}"')
def step_fill_field(context, label, value):
    fill_input_with_label(context, label, value)


@when('je coche la case "{}"')
def step_check_box(context, label):
    find_checkbox_label(context, label).click()


@when('je choisis "{}" pour "{}"')
def step_choose_option(context, value, legend):
    find_option_with_label(context, legend, value).click()


@when('je clique sur "{}"')
def step_click_on_option(context, label):
    context.browser.find_element(By.LINK_TEXT, label).click()


@when("je soumets le formulaire")
def step_submit_form(context):
    context.browser.find_element(By.XPATH, '//form//*[@type="submit"]').click()


@then('un email a été envoyé à "{}"')
def step_send_email(context, email):
    context.mocks["sib"].assert_called_with(email, payload=ANY)
