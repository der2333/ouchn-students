# OUCHN 学习平台自动登录工具

自动化登录国家开放大学(ouchn.cn)学习平台，遍历学生课程并模拟学习活动。

## 功能特点

- 读取学生账号密码 CSV 文件批量登录
- 使用 Playwright 浏览器自动化
- 每学期每学生限制 30 次登录
- 自动遍历课程并触发学习活动
- 支持专升本学生切换
- 反检测措施（隐藏 webdriver 属性）
- 打包后从可执行程序所在目录读取外部账号表

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
├── main.spec            # PyInstaller 打包配置
└── pyproject.toml       # 项目依赖
```

## 依赖

- Python 3.14+
- playwright
- pyinstaller（打包用）

## 使用方法

### 1. 配置账号

把 `学生账号.csv` 放在程序同目录，格式：

```
学号,密码
20230001,password123
```

本地源码运行时，程序会读取项目目录下的 `学生账号.csv`；打包后运行时，程序会读取可执行文件所在目录下的 `学生账号.csv`。账号表不需要打包进可执行程序。

### 2. 安装依赖

```bash
uv sync
```

### 3. 运行

```bash
uv run python main.py
```

运行后会在程序同目录读写 `login_count.json`，用于记录每个学生本学期的登录次数。

## 打包命令

当前项目使用 PyInstaller，`学生账号.csv` 和 `login_count.json` 都作为外部文件使用，不需要加入 `datas`。

```bash
uv run pyinstaller main.spec
```

打包完成后，把账号表放到 `dist` 目录：

```text
dist/
├── main
└── 学生账号.csv
```

## 注意事项

- 登录次数每学期自动重置
- 滑块验证功能已注释（可直接启用）
- 请确保账号密码正确，避免锁定
- 打包前建议先用 `uv run python main.py` 本地测试运行
- 如果提示读取 `学生账号.csv` 出错，检查提示中的实际读取路径，并确认该路径下存在账号表
