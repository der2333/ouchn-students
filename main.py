def main():
    from playwright.sync_api import sync_playwright
    from browser_launcher import launch_local_browser
    from student_login import student_login
    from students import load_students

    # 读取学生账号（学生账号.xlsx 或 学生账号.csv，xlsx 优先）
    try:
        students_list: dict[str, str] = load_students()
    except FileNotFoundError as exc:
        print(exc)
        input("按回车键退出程序...")
        return
    except Exception as exc:
        print(f"读取学生账号文件出错：{exc}")
        input("按回车键退出程序...")
        return

    if not students_list:
        print("学生账号为空，无需自动登录。")
        input("按回车键退出程序...")
        return

    with sync_playwright() as p:
        # 使用本机已安装的 Chrome / Edge，不依赖打包内置的浏览器内核
        try:
            browser = launch_local_browser(p)
        except RuntimeError as exc:
            print(exc)
            input("按回车键退出程序...")
            return

        for login_name, password in students_list.items():
            try:
                student_login(login_name, password, browser)
                print(f"{login_name} 登录成功")
            except Exception:
                if browser.contexts:
                    browser.contexts[0].close()
                print(f"跳过：{login_name}，密码不正确或网页加载异常")

        browser.close()

    input("运行完成，按回车键退出程序...")


if __name__ == "__main__":
    main()
