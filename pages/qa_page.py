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

    def get_listed_jobs(self, department):
        """
        Returns a list of visible job elements from the jobs list section.
        Scrolls to the section if not immediately visible.
        :param department: The department to wait for filter will be applied.
        :return: list[WebElement]: List of job container elements.
        """
        self.scroll_and_find_element(self.JOB_LIST)
        self.wait_text_to_be_present_in_element(self.JOB_LIST_ITEM_DEPT, department)
        return self.get_elements(self.JOB_LIST)

    def get_job_details(self, job_element):
        """
        Extracts title, department, and location text from a single job element.
        :param job_element: WebElement representing one job listing.
        :return: dict: Dictionary with 'title', 'department', and 'location' keys.
        """
        title = job_element.find_element(*self.JOB_TITLE).text
        dept = job_element.find_element(*self.JOB_DEPT).text
        loc = job_element.find_element(*self.JOB_LOC).text
        return {"title": title, "department": dept, "location": loc}

    def click_view_role(self):
        """
        Scrolls to the jobs list and clicks the 'View Role' link for the first listed job.
        """
        container = self.get_element(self.JOB_LIST)
        ActionChains(self.driver).move_to_element(container).perform()
        self.wait.until(EC.element_to_be_clickable(self.VIEW_ROLE)).click()

    def get_selected_job_title(self):
        """
        Retrieves the job title text from the first job in the list.
        :return: str: The job title text.
        """
        return self.get_element(self.JOB_LIST_ITEM_TITLE).text

    def switch_to_new_tab(self):
        """
        Switches Selenium's context to the newly opened browser tab.
        Waits until a second tab is available.
        """
        self.wait.until(lambda driver: len(driver.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
