import csv
from playwright.sync_api import sync_playwright

from student_login import student_login


def main():
    students_list: dict[str, str] = {}
    with open("studentsList.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            students_list.update({row[0]: f"Ouchn@{row[1]}"})

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            executable_path="C:\\Users\\13388\\AppData\\Local\\ms-playwright\\chromium-1161\\chrome-win\\chrome.exe",
            # executable_path="/Users/fyf/Library/Caches/ms-playwright/chromium-1161/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
        )
        for login_name, password in students_list.items():
            try:
                student_login(login_name, password, browser)
            except Exception as _:
                browser.contexts[0].close()
                print(f"登录失败，跳过 {login_name}")


if __name__ == "__main__":
    main()
