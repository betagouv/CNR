from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def before_all(context):
    options = Options()
    options.headless = True

    context.browser = webdriver.Firefox(options=options)
    context.browser.set_window_size(1200, 900)
    context.browser.implicitly_wait(1)

def after_all(context):
    context.browser.quit()
