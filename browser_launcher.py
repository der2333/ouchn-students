"""启动本机已安装的浏览器（不使用打包内置的 Chromium）。

程序运行时依次尝试本机的 Google Chrome、Microsoft Edge，
任一可用即用其启动。因此打包产物中不需要包含浏览器内核，
用户也无需执行 ``playwright install``。
"""

from playwright.sync_api import Browser, Playwright

# 依次尝试的浏览器通道：优先 Chrome，不可用时回退 Edge
BROWSER_CHANNELS: list[tuple[str, str]] = [
    ("chrome", "Google Chrome"),
    ("msedge", "Microsoft Edge"),
]

# 启动参数（反自动化检测）
LAUNCH_ARGS: list[str] = [
    "--disable-blink-features=AutomationControlled",
]


def _short_error(exc: Exception) -> str:
    """压缩异常信息为单行短文本，便于在提示中展示。"""
    return " ".join(str(exc).split())[:200]


def launch_local_browser(playwright: Playwright, headless: bool = False) -> Browser:
    """启动本机 Chrome / Edge 并返回 Browser 实例。

    按 :data:`BROWSER_CHANNELS` 的顺序依次尝试，全部失败时抛出 RuntimeError，
    异常信息中包含每种浏览器的失败原因，便于用户排查。
    """
    failures: list[str] = []
    for channel, label in BROWSER_CHANNELS:
        try:
            browser = playwright.chromium.launch(
                channel=channel,
                headless=headless,
                args=LAUNCH_ARGS,
            )
        except Exception as exc:  # 未安装或启动失败，继续尝试下一个
            failures.append(f"  - {label}：{_short_error(exc)}")
            continue
        print(f"已启动本机 {label}（版本 {browser.version}）")
        return browser

    reason = "\n".join(failures)
    raise RuntimeError(
        "未能启动浏览器：请先在本机安装 Google Chrome 或 Microsoft Edge。\n"
        f"尝试结果：\n{reason}"
    )
