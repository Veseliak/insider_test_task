from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_page import QAPage

def test_e2e(browser):
    """
    Step 1: Visit home
    Step 2: Navigate to Company > Careers
    Step 3: Check sections
    Step 4: Apply filter & verify jobs
    Step 5: Click View Role and check that you redirects to correct page
    """
    home = HomePage(browser)
    home.go_to_home()
    home.go_to_careers()
    careers = CareersPage(browser)
    careers.check_sections()
    careers.navigate_to_see_all_qa_jobs()
    qa = QAPage(browser)
    qa.apply_filters("Istanbul, Turkiye", "Quality Assurance")
    qa.verify_jobs("Quality Assurance", "Istanbul, Turkiye")
    qa.click_view_role_and_check_that_shown_correct_page()