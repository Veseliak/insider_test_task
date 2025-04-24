from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class QAPage(BasePage):
    FILTER_LOC = (By.XPATH, "//select[@name='filter-by-location']")
    FILTER_DEPT = (By.XPATH, "//select[@name='filter-by-department']")
    JOB_LIST = (By.CSS_SELECTOR, "div.position-list-item")
    JOB_TITLE = (By.CSS_SELECTOR, "p.position-title")
    JOB_DEPT = (By.CSS_SELECTOR, "span.position-department")
    JOB_LOC = (By.CSS_SELECTOR, "div.position-location")
    VIEW_ROLE = (By.XPATH, "//a[contains(text(), 'View Role')][1]")
    JOB_LIST_ITEM_TITLE = (By.XPATH, "//*[@id='jobs-list']/div[1]/div/p")
    LEVER_CO_TITLE = (By.XPATH, "//h2[contains(text(), 'Quality Assurance')]")
    TITLE = (By.XPATH, "//title")
    QA_DEPT_ITEM = (By.XPATH, f"//option[contains(text(), 'Quality Assurance')]")
    ISTANBUL_LOC_ITEM = (By.XPATH, f"//option[contains(text(), 'Istanbul, Turkiye')]")
    JOB_LIST_ITEM_DEPT = (By.XPATH, "//*[@id='jobs-list']/div[1]/div/span")

    def apply_filters(self, location, department):
        """
        This function applies filters on the page by selecting the specified location and department.
        :param location: The location to select from the location filter dropdown.
        :param department: The department to select from the department filter dropdown.
        Raises:TimeoutException: If the filters or options are not visible or interactable within the timeout period.
        """
        self.wait_visibility_of_element_located(self.ISTANBUL_LOC_ITEM)
        self.wait_visibility_of_element_located(self.QA_DEPT_ITEM)
        Select(self.get_element(self.FILTER_LOC)).select_by_visible_text(location)
        Select(self.get_element(self.FILTER_DEPT)).select_by_visible_text(department)

    def verify_jobs(self, title_text, location):
        """
        This function verifies that jobs listed on the page match the given title and location filters.
        :param title_text: The title text to be verified in each job listing.
        :param location: The location text to be verified in each job listing.
        Raises: AssertionError: If no jobs are found, or if a job does not match the expected title or location.
        """
        self.scroll_and_find_element(self.JOB_LIST)
        self.wait_text_to_be_present_in_element(self.JOB_LIST_ITEM_DEPT, title_text)
        jobs = self.get_elements(self.JOB_LIST)
        assert jobs, "No jobs found"
        for job in jobs:
            title = job.find_element(*self.JOB_TITLE).text
            dept = job.find_element(*self.JOB_DEPT).text
            loc = job.find_element(*self.JOB_LOC).text
            assert title_text in title
            assert title_text in dept
            assert location in loc

    def click_view_role_and_check_that_shown_correct_page(self):
        """
        This function clicks the "View Role" button and verifies that the correct job page is displayed.
        """
        role_title = self.get_element(self.JOB_LIST_ITEM_TITLE).text
        container = self.get_element(self.JOB_LIST)
        ActionChains(self.driver).move_to_element(container).perform()
        self.wait.until(EC.element_to_be_clickable(self.VIEW_ROLE)).click()
        self.wait.until(lambda driver: len(driver.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.wait.until(EC.url_contains("jobs.lever.co"))
        self.wait.until(EC.title_contains(role_title))
        assert "jobs.lever.co" in self.driver.current_url
