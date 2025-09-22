def main():
    import csv
    import json
    import os
    from playwright.sync_api import sync_playwright
    from student_login import student_login

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

    # 读取或初始化登录次数json，结构：{"学号": {"count": int, "last_date": "YYYY-MM-DD"}}
    from datetime import datetime

    today = datetime.now().strftime("%Y-%m-%d")
    login_count_path = "login_count.json"
    if os.path.exists(login_count_path):
        with open(login_count_path, "r", encoding="utf-8") as f:
            try:
                login_count = json.load(f)
            except Exception:
                login_count = {}
    else:
        login_count = {}

    # 补充新学生，初始化为{"count": 0, "last_date": ""}
    for login_name in students_list.keys():
        if login_name not in login_count or not isinstance(
            login_count[login_name], dict
        ):
            login_count[login_name] = {"count": 0, "last_date": ""}

    # 只处理登录次数未满20次的学生
    students_to_login = {
        k: v
        for k, v in students_list.items()
        if login_count.get(k, {}).get("count", 0) < 20
    }
    if not students_to_login:
        print("所有学生登录次数均已达上限，无需自动登录。")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            ],
            executable_path="C:\\Users\\13388\\AppData\\Local\\ms-playwright\\chromium-1161\\chrome-win\\chrome.exe",
        )

        for login_name, password in students_to_login.items():
            try:
                student_login(login_name, password, browser)
                # 判断今天是否已计数
                last_date = login_count[login_name].get("last_date", "")
                if last_date != today:
                    login_count[login_name]["count"] = (
                        login_count[login_name].get("count", 0) + 1
                    )
                    login_count[login_name]["last_date"] = today
                    print(
                        f"{login_name} 登录成功，当前累计登录次数：{login_count[login_name]['count']}"
                    )
                else:
                    print(
                        f"{login_name} 今天已登录过，累计登录次数未增加，当前为：{login_count[login_name]['count']}"
                    )
                # 每次登录后立即写入json文件
                with open(login_count_path, "w", encoding="utf-8") as f:
                    json.dump(login_count, f, ensure_ascii=False, indent=2)
            except Exception:
                browser.contexts[0].close()
                print(f"跳过：{login_name}，登录失败，请检查学号或密码是否正确。")

    input("运行完成，按回车键退出程序...")


if __name__ == "__main__":
    main()
