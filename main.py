def main():
    import csv
    import json
    import os
    from playwright.sync_api import sync_playwright
    from student_login import student_login
    from datetime import datetime

    students_list: dict[str, str] = {}
    try:
        with open("学生账号.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                students_list.update({row[0]: row[1]})
    except Exception:
        print('读取"学生账号.csv文件"出错，请确保文件存在。')
        input("按回车键退出程序...")

    # 读取或初始化登录次数json，结构：
    # {
    #   "学号": {"count": int, "last_date": "yyyy-mm-dd"},
    #   "__meta__": {"last_reset_semester": "2025-Spring"}
    # }
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

    # 学期判断函数：返回学期标识字符串，例如 "2025-Spring" 或 "2025-Fall"
    def current_semester(dt: datetime) -> str:
        year = dt.year
        month = dt.month
        # 春季学期：3-6月 -> Spring
        if 3 <= month <= 6:
            return f"{year}-Spring"
        # 秋季学期：9月到次年1月 -> Fall
        # Note: months 9..12 belong to current year's Fall, month 1 belongs to previous Fall's semester period
        if month >= 9 or month == 1:
            # For January, the semester is the Fall of the previous year
            sem_year = year if month >= 9 else year - 1
            return f"{sem_year}-Fall"
        # 其他月份（2,7,8）：不在定义的学期区间，返回最近的学期标签
        # 2月视为上学期（previous Fall），7-8月视为刚过的 Spring
        if month == 2:
            return f"{year - 1}-Fall"
        # month in (7,8)
        return f"{year}-Spring"

    sem = current_semester(datetime.now())

    # 如果 __meta__ 中记载的上次重置学期与当前学期不同，则在本学期首次运行时重置所有学生的 count
    meta = login_count.get("__meta__", {}) or {}
    last_reset = meta.get("last_reset_semester", "")
    if last_reset != sem:
        # 将所有已存在学生的 count 置0（但保留 last_date 字段），并记录重置学期
        for k in list(login_count.keys()):
            if k == "__meta__":
                continue
            if not isinstance(login_count.get(k), dict):
                login_count[k] = {"count": 0, "last_date": ""}
            else:
                login_count[k]["count"] = 0
        login_count["__meta__"] = {"last_reset_semester": sem}
        # 立即写回文件
        try:
            with open(login_count_path, "w", encoding="utf-8") as f:
                json.dump(login_count, f, ensure_ascii=False, indent=2)
            print(f"检测到新学期({sem})，已将所有学生登录次数重置为0。")
        except Exception:
            print("尝试写入 login_count.json 失败，重置未保存。请检查文件权限。")

    # 清理已不存在的学生：从 login_count 中删除那些不在学生账号表的学号
    existing_students = set(students_list.keys())
    for k in list(login_count.keys()):
        if k == "__meta__":
            continue
        if k not in existing_students:
            del login_count[k]

    # 补充新学生，初始化为{"count": 0, "last_date": ""}
    for login_name in students_list.keys():
        if login_name == "":
            continue

        if login_name not in login_count or not isinstance(
            login_count[login_name], dict
        ):
            login_count[login_name] = {"count": 0, "last_date": ""}

    # 写回 login_count.json，保存删除/新增的同步结果
    try:
        with open(login_count_path, "w", encoding="utf-8") as f:
            json.dump(login_count, f, ensure_ascii=False, indent=2)
    except Exception:
        print("尝试写入 login_count.json 失败，变更未保存。请检查文件权限。")

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
                print(f"跳过：{login_name}，密码不正确或网页加载异常")

    input("运行完成，按回车键退出程序...")


if __name__ == "__main__":
    main()
