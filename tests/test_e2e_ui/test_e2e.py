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
    jobs = qa.get_listed_jobs("Quality Assurance")
    assert jobs, "No jobs found"
    for job in jobs:
        details = qa.get_job_details(job)
        assert "Quality Assurance" in details["title"]
        assert "Quality Assurance" in details["department"]
        assert "Istanbul, Turkiye" in details["location"]
    role_title = qa.get_selected_job_title()
    qa.click_view_role()
    qa.switch_to_new_tab()
    assert "jobs.lever.co" in browser.current_url
    assert role_title in browser.title