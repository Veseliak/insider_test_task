from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CareersPage(BasePage):
    LOCATIONS = (By.XPATH, "//*[@id='career-our-location']")
    SEE_ALL_TEAMS_BUTTON = (By.XPATH, "//a[contains(text(), 'See all teams')]")
    TEAMS = (By.XPATH, "//h3[contains(text(), 'Find your calling')]")
    LIFE_AT_INSIDER = (By.XPATH, "//h2[contains(text(), 'Life at Insider')]")
    SEE_ALL_QA_JOBS = (By.XPATH, "//a[contains(text(), 'See all QA jobs')]")

    def check_sections(self):
        """
        This function verify data in Careers page
        """
        try:
            assert self.scroll_and_find_element(self.TEAMS), "Teams block not found"
            assert self.scroll_and_find_element(self.SEE_ALL_TEAMS_BUTTON), "See all teams teams button not found"
            assert self.scroll_and_find_element(self.LOCATIONS), "Locations block not found"
            assert self.scroll_and_find_element(self.LIFE_AT_INSIDER), "Life at Insider block not found"
        except TimeoutException as e:
            raise AssertionError(f"Failed to find one or more blocks. Details: {str(e)}")

    def navigate_to_see_all_qa_jobs(self):
        """
        This function navigate to QA Careers page and click See all QA jobs
        """
        self.go_to('https://useinsider.com/careers/quality-assurance/')
        self.click(self.SEE_ALL_QA_JOBS)