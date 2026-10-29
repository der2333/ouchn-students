# OUCHN 学习平台自动登录工具

自动化登录国家开放大学(ouchn.cn)学习平台，遍历学生课程并模拟学习活动。

## 功能特点

- 读取学生账号文件（Excel `.xlsx` 或 `.csv`）批量登录
- 使用 Playwright 浏览器自动化
- 直接调用本机已安装的 Chrome / Edge，无需下载内置浏览器内核
- 自动遍历课程并触发学习活动
- 支持专升本学生切换
- 反检测措施（隐藏 webdriver 属性）

## 项目结构

```
ouchn-students/
├── main.py              # 主程序入口
├── students.py          # 读取学生账号（xlsx / csv）
├── browser_launcher.py  # 启动本机 Chrome / Edge
├── student_login.py     # 学生登录模块
├── process_course.py    # 课程处理模块
├── init_page.py         # 页面初始化（反检测脚本）
├── slider_validation.py # 滑块验证（已禁用）
├── main.spec            # PyInstaller 打包配置
├── version_info.txt     # 打包用版本信息
├── 学生账号.xlsx / .csv  # 学生账号数据（二选一，同时存在时用 xlsx）
└── pyproject.toml       # 项目依赖
```

## 依赖

- Python 3.14（由 `.python-version` 固定，uv 自动安装）
- playwright
- openpyxl（读取 xlsx）
- requests
- pyinstaller（打包用）

运行前提：本机已安装 Google Chrome 或 Microsoft Edge（程序优先使用 Chrome，不可用时回退 Edge）。

## 使用方法

### 1. 配置账号

在程序所在目录放一个 `学生账号.xlsx` 或 `学生账号.csv`，两者同时存在时优先使用 xlsx。

**xlsx 格式**：第一个工作表的 A 列学号、B 列密码，首行表头可有可无：

| 学号 | 密码 |
| --- | --- |
| 20230001 | password123 |
| 20230002 | password456 |

**csv 格式**：

```
学号,密码
20230001,password123
```

说明：

- 表头行（`学号` / `密码` / `name` / `password` 等）会自动识别并跳过，没有表头也能正常读取
- 学号、密码的首尾空格会自动去掉
- 学号或密码为空的行会被跳过，并在控制台提示跳过了多少行
- xlsx 中按数字保存的学号会按整数读取，不会出现 `20230001.0`
- csv 支持 UTF-8（含 BOM）与 ANSI(GBK) 编码

### 2. 安装依赖

```bash
uv sync
```

> 项目通过 `.python-version` 固定使用 Python 3.14，首次 `uv sync` 会自动下载 3.14 解释器与依赖。
> 无需执行 `playwright install`：程序使用本机浏览器，不下载 Playwright 内置浏览器。

### 3. 运行

```bash
uv run python main.py
```

## 打包

使用 PyInstaller 打包为单文件 exe，产物中**不含浏览器内核**：

```bash
uv run pyinstaller main.spec --clean --noconfirm
```

产物：`dist/OUCHN学习助手.exe`，双击即可运行。

- `main.spec`：只收集 Playwright 驱动（`node.exe` + `cli.js`），不收集任何浏览器；openpyxl 由导入分析自动打包
- `version_info.txt`：产品名、公司名、版本号等文件属性，可减少杀毒软件误报
- 程序通过 `print` / `input` 与用户交互，因此保留控制台窗口（`console=True`）

## 注意事项

- 学生账号文件放在 exe / main.py 所在目录；该目录没有时也会查找当前工作目录
- 程序优先启动本机 Chrome，未安装时自动回退到 Edge；两者都不存在时会提示先安装
- 启动时使用临时用户配置目录，不会读取或修改你日常浏览器的书签、密码与登录状态
- 不限制登录次数与登录天数
- 滑块验证功能已注释（可直接启用）
- 请确保账号密码正确，避免锁定
- 打包前建议先用 `python main.py` 本地测试运行
