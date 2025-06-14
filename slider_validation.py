import re
from urllib import request
import ddddocr
from playwright.sync_api import Page


def slider_validation(index_page: Page):
    bg_style = index_page.locator("body .geetest_bg").get_attribute("style")
    slide_style = index_page.locator("body .geetest_slice_bg").get_attribute("style")
    if bg_style is None or slide_style is None:
        return
    p = r'background-image: url\("(.*?)"\);'
    bg_url: str = re.findall(p, bg_style, re.S)[0]
    slide_url: str = re.findall(p, slide_style, re.S)[0]

    # 下载滑块图片、背景图片
    request.urlretrieve(bg_url, "tmp/bg.png")
    request.urlretrieve(slide_url, "tmp/slide.png")

    # 使用ddddocr计算出目标位置
    det = ddddocr.DdddOcr(det=False, ocr=False)
    with open("tmp/bg.png", "rb") as f:
        bg_img = f.read()
    with open("tmp/slide.png", "rb") as f:
        slide_img = f.read()
    res = det.slide_match(slide_img, bg_img, simple_target=True)
    # print(res["target"][0])

    # 获取滑块位置，并计算拖动的起始和结束位置
    slider_box = index_page.locator("body .geetest_btn").bounding_box()
    if slider_box is None:
        print("滑块验证失败，未能获取滑块位置")
        return
    start_x = slider_box["x"] + slider_box["width"] / 2
    start_y = slider_box["y"] + slider_box["height"] / 2
    end_x = start_x + res["target"][0]

    # 执行拖动操作
    index_page.mouse.move(start_x, start_y)
    index_page.mouse.down()
    index_page.mouse.move(
        end_x, start_y, steps=100
    )  # steps参数使移动更平滑，模拟人类操作
    index_page.mouse.up()

    index_page.wait_for_timeout(2000)  # 等待验证完成
    if (
        index_page.locator(".geetest_result_tips").is_visible()
        and index_page.locator(".geetest_result_tips").inner_text()
        == "验证失败 请重新尝试"
    ):
        slider_validation(index_page)
