from playwright.sync_api import BrowserContext

from init_page import init_page


def process_course(context: BrowserContext, course_url: str) -> None:
    try:
        course_page = context.new_page()
        init_page(course_page)
        course_page.goto(f"https://lms.ouchn.cn{course_url}")
        course_page.locator("#course-section").click()
        course_page.locator(".learning-activity a").first.click()
        for i in range(5):
            course_page.locator(".next-btn").click()
            course_page.wait_for_timeout(3000)
        course_page.close()
    except Exception as _:
        if len(context.pages) > 1:
            context.pages[1].close()
        process_course(context, course_url)
