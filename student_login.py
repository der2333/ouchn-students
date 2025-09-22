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
    index_page.locator("#form_button").click()
    index_page.wait_for_timeout(2000)  # 等待2秒钟，确保滑块验证加载完成

    # 滑块验证
    if index_page.get_by_text("1/2").count() == 1:
        slider_validation(index_page)
        index_page.wait_for_timeout(3000)
        slider_validation(index_page)
    else:
        slider_validation(index_page)

    index_page.wait_for_selector("a.ng-binding.ng-scope")

    # 如果超过10个课程，选择显示100页
    if index_page.locator(".select2-choice").is_visible():
        index_page.locator(".select2-choice").click()
        index_page.locator(".select2-results-dept-0").last.click()
        index_page.wait_for_timeout(3000)

    # 刷点课次数次数
    # 获取课程列表
    course_list = index_page.locator("a.ng-binding.ng-scope").all()
    # 遍历课程列表，并执行回帖操作
    for course in course_list:
        course_url = course.get_attribute("href")
        if course_url is None:
            continue

        # 处理单个课程
        # try:
        process_course(context, course_url)
        # except Exception as _:
        #     if len(context.pages) > 1:
        #         context.pages[1].close()
        #     print(f"点课出现错误 {course_url}: 跳过当前课程")
