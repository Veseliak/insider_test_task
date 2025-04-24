import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def click(self, locator):
        """
        This function click on some locator
        :param locator: locator
        """
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def get_element(self, locator):
        """
        This function waits until the specified element is visible on the page and returns it.
        :param locator: locator
        :return: WebElement: The Selenium WebElement once it becomes visible.
        Raises:
        TimeoutException: If the element does not become visible within the wait time.
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    def get_elements(self, locator):
        """
        This function waits until all elements matching the specified locator are visible and returns them.
        :param locator: locator
        :return: list[WebElement]: A list of Selenium WebElements once they become visible.
        Raises:
        TimeoutException: If the elements do not become visible within the wait time.
        """
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def scroll_and_find_element(self, locator, max_scrolls=15):
        """
        This function scrolls the page to find an element by repeatedly scrolling and checking for its presence and visibility.
        :param locator: locator
        :param max_scrolls: Maximum number of scroll attempts before raising an exception.
        :return: WebElement: The located and visible element.
        Raises:
        TimeoutException: If the element cannot be found and made visible after the specified
                          number of scroll attempts.
        """
        scrolls = 0
        while scrolls < max_scrolls:
            try:
                element = self.wait.until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                self.wait.until(EC.visibility_of(element))
                return element
            except:
                self.driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(1)
                scrolls += 1
        raise TimeoutException(f"Could not find element after {max_scrolls} scrolls: {locator}")

    def go_to(self, url):
        """
        This function navigates the browser to the specified URL.
        :param url: url
        """
        self.driver.get(url)

    def wait_visibility_of_element_located(self, locator):
        """
        This function waits up to 10 seconds for an element located by the given locator to become visible on the page.
        :param locator: locator
        :return: WebElement: The visible web element.
        Raises:
        TimeoutException: If the element does not become visible within 10 seconds.
        """
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))

    def wait_text_to_be_present_in_element(self, locator, text):
        """
        This function waits until the specified text is present in the element located by the given locator.
        :param locator: locator
        :param text: The text to wait for within the target element.
        :return: WebElement: TimeoutException: If the element is present
        """
        return self.wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_element_to_be_clickable(self, locator):
        """
        This function waits until the element located by the given locator is clickable.
        :param locator: locator
        :param text: The text to wait for within the target element.
        :return: TimeoutException: If the element is not clickable within the timeout period.
        """
        return WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(locator))