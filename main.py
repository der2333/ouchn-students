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
            executable_path="/Users/fyf/Library/Caches/ms-playwright/chromium-1161/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
        )
        for login_name, password in students_list.items():
            try:
                student_login(login_name, password, browser)
            except Exception as e:
                print(f"Error logging in {login_name}: {e}")


if __name__ == "__main__":
    main()
