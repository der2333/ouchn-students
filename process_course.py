import random
import time
from playwright.sync_api import BrowserContext, Request
import requests

from init_page import init_page


# 设置请求监听器
def log_request(request: Request) -> None:
    if request.url == "https://lms.ouchn.cn/statistics/api/learning-activity":
        # 获取请求的post数据
        post_data = request.post_data
        if post_data is None:
            print("No payload data")
            return

        # 使用 APIRequestContext 重新发送请求
        num = 5
        try:
            cookies = request.all_headers()["cookie"]
        except Exception:
            cookies = ""
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Cookie": cookies,
        }
        for _ in range(num):
            requests.post(
                url=request.url,
                data=post_data,
                headers=headers,
            )
            time.sleep(random.uniform(1.0, 2.0))


def process_course(context: BrowserContext, course_url: str) -> None:
    try:
        course_page = context.new_page()
        init_page(course_page)
        course_page.on("request", log_request)
        course_page.goto(f"https://lms.ouchn.cn{course_url}")
        course_page.locator("#course-section").click()
        course_page.locator(".learning-activity a").first.click()

        # for i in range(5):
        #     course_page.locator(".next-btn").click()
        #     course_page.wait_for_timeout(3000)
        # course_page.close()
        course_page.wait_for_selector(".next-btn")
        course_page.close()
    except Exception:
        pass
