# OUCHN 学习平台自动登录工具

自动化登录国家开放大学(ouchn.cn)学习平台，遍历学生课程并模拟学习活动。

## 功能特点

- 读取学生账号密码 CSV 文件批量登录
- 使用 Playwright 浏览器自动化
- 每学期每学生限制 20 次登录
- 自动遍历课程并触发学习活动
- 支持专升本学生切换
- 反检测措施（隐藏 webdriver 属性）

## 项目结构

```
ouchn-students/
├── main.py              # 主程序入口
├── student_login.py     # 学生登录模块
├── process_course.py    # 课程处理模块
├── init_page.py         # 页面初始化（反检测脚本）
├── slider_validation.py # 滑块验证（已禁用）
├── 学生账号.csv          # 学生账号数据
├── login_count.json     # 登录次数记录
└── pyproject.toml       # 项目依赖
```

## 依赖

- Python 3.10+
- playwright
- requests
- nuitka（打包用）

## 使用方法

### 1. 配置账号

编辑 `学生账号.csv`，格式：
```
学号,密码
20230001,password123
```

### 2. 安装依赖

```bash
uv sync
playwright install chromium
```

### 3. 运行

```bash
python main.py
```

## 打包命令

exe 体积较大（~150MB+），但可一键运行。使用 `--no-upx` 和完整版本信息减少杀毒软件误报。

```bash
python -m nuitka --mode=onefile ^
  --playwright-include-browser=chromium-1187 ^
  --no-upx ^
  --windows-company-name="xichen" ^
  --windows-product-name="OUCHN 学习助手" ^
  --windows-file-version="1.0.0.0" ^
  --windows-product-version="1.0.0.0" ^
  --windows-file-description="国家开放大学学习平台自动登录工具" ^
  --windows-copyright="Copyright © 2026" ^
  main.py
```

## 注意事项

- 登录次数每学期自动重置
- 滑块验证功能已注释（可直接启用）
- 请确保账号密码正确，避免锁定
- 打包前建议先用 `python main.py` 本地测试运行
