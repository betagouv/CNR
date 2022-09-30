from unittest.mock import Mock

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from public_website import email_provider


def before_all(context):
    options = Options()
    options.headless = True

    context.browser = webdriver.Firefox(options=options)
    context.browser.set_window_size(1200, 900)
    context.browser.implicitly_wait(1)

    context.mocks = {}

    context.mocks["sib"] = Mock()

    email_provider.send_payload_to_send_in_blue = context.mocks["sib"]


def after_feature(context, feature):
    for mock in context.mocks.values():
        mock.reset_mock()


def after_all(context):
    context.browser.quit()
