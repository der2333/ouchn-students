import csv
from playwright.sync_api import sync_playwright

from student_login import student_login


def main():
    students_list: dict[str, str] = {}
    try:
        with open("学生账号.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                students_list.update({row[0]: row[1]})
    except Exception:
        print("读取学生账号.csv文件出错，请确保文件存在并包含正确的格式。")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            # executable_path="C:\\Users\\13388\\AppData\\Local\\ms-playwright\\chromium-1161\\chrome-win\\chrome.exe",
            # executable_path="/Users/fyf/Library/Caches/ms-playwright/chromium-1161/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
        )
        for login_name, password in students_list.items():
            try:
                student_login(login_name, password, browser)
            except Exception:
                browser.contexts[0].close()
                print(f"登录失败，跳过：{login_name}")
                # print(f"错误信息: {e}")

    input("运行完成，按回车键退出程序...")


if __name__ == "__main__":
    main()
