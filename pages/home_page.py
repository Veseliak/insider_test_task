from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    COMPANY_MENU = (By.XPATH, "//a[contains(text(), 'Company')] ")
    CAREERS_LINK = (By.XPATH, "//a[contains(text(), 'Careers')] ")
    ACCEPT_ALL_IN_COOKIE_BANNER = (By.XPATH, "//a[contains(text(), 'Accept All')]")

    def press_accept_all_in_cookie_banner(self):
        """
                This function press Accept All in cookie banner
        """
        try:
            self.wait_element_to_be_clickable(self.ACCEPT_ALL_IN_COOKIE_BANNER).click()
            print("Cookies banner closed.")
        except TimeoutException:
            print("No cookies banner found.")

    def go_to_home(self):
        """
        This function navigate to home page
        """
        self.go_to("https://useinsider.com/")
        self.press_accept_all_in_cookie_banner()
        assert "Insider" in self.driver.title

    def go_to_careers(self):
        """
        This function navigate to Careers page
        """
        self.click(self.COMPANY_MENU)
        self.click(self.CAREERS_LINK)