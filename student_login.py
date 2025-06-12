from playwright.sync_api import Browser

from slider_validation import slider_validation
from init_page import init_page
from process_course import process_course


def student_login(login_name: str, password: str, browser: Browser) -> None:
    context = browser.new_context()
    index_page = context.new_page()
    if len(browser.contexts) > 1:
        browser.contexts[0].close()
    init_page(index_page)
    index_page.goto("https://lms.ouchn.cn/user/courses#/")
    index_page.wait_for_load_state("networkidle")

    # 输入用户名和密码
    index_page.locator("#loginName").fill(login_name)
    index_page.locator("#password").fill(password)
    index_page.locator("#agreeCheckBox").click()

    # 滑块验证
    slider_validation(index_page)

    # 刷点课次数次数
    # 获取课程列表
    course_list = index_page.locator("a.ng-binding.ng-scope").all()
    # 遍历课程列表，并执行回帖操作
    for course in course_list:
        course_url = course.get_attribute("href")
        if course_url is None:
            continue

        # 处理单个课程
        try:
            process_course(context, course_url)
        except Exception as e:
            print(f"Error processing course {course_url}: {e}")

    print("login:", login_name, "password:", password)
    input("Press Enter to continue...")
