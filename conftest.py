import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests: chrome or firefox")

@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser").lower()
    driver = None

    if browser_name == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
    else:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

    driver.maximize_window()
    yield driver

    if request.node.rep_call.failed:
        driver.save_screenshot("failed_test.png")
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    # Hook to capture test failure state
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)