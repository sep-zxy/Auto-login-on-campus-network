# 校园网 Portal 认证自动化

**Playwright · Headless Edge · State-aware Login · Local Configuration**

基于 Python / Playwright 的校园网认证自动化工具，使用无头 Microsoft Edge 执行真实 Portal 页面的登录流程。将在线状态检测、表单填充、运营商选择与后台提交串成可重复执行的流程，配套 AutoHotkey 图形化配置入口。

## 执行机制

```text
本地配置 → 打开 Portal → 检查在线状态
                         ├─ 已在线 → 跳过重复登录
                         └─ 未在线 → 填充凭据 → 选择认证域 → 提交表单
```

- **Browser-driven Authentication**：通过浏览器执行页面及其认证脚本，沿用页面原有的登录交互。
- **State-aware Execution**：依据退出按钮的可见状态判断当前页面是否已登录，减少重复提交。
- **Headless Automation**：后台运行 Edge，无需手动打开并操作认证页面。
- **Configuration Separation**：账号、密码和认证域保存在本地 JSON，配置界面与登录脚本共享读取。

## 适配与迁移

项目实践来自深澜（Srun）Portal 认证页面。迁移到其他部署时，需要对齐以下入口和页面契约；当前实现未提供自动识别学校或通用协议适配器。

| 适配点 | 当前实现位置 |
| --- | --- |
| Portal 入口 | `autologin.py` 中的 `page.goto(...)` |
| 在线状态 | `#logout` 的可见状态 |
| 账号与密码 | `#username`、`#password` |
| 认证域 / 运营商 | `#domain`，配置值为页面选项的显示文本 |
| 提交动作 | `#login-account` |

不同部署可能采用不同入口、页面模板、认证域或额外验证流程，需要逐项核对。当前代码在点击提交后输出执行提示，尚未进行提交后的独立连通性校验。


## 第一部分：功能介绍

本项目包含两个核心组件：

1.  **图形化配置工具 (AutoHotkey)**：
    * 提供一个简洁的图形界面，让用户可以轻松输入并保存自己的校园网账号、密码和运营商信息。
    * 配置信息以 `config.json` 保存在本地，供配置界面和登录脚本共享读取。
    * 启动时会自动读取现有配置，方便用户修改。

2.  **自动登录脚本 (Python)**：
    * 核心的登录执行程序，使用 Playwright 库驱动一个无头浏览器 (Headless Microsoft Edge) 在后台运行，用户无感知。
    * 启动时会自动读取 `config.json` 文件中的配置信息。
    * **在线状态检测**：在执行登录前，会先访问登录页面并检查是否已经处于登录状态。如果已登录，则会跳过操作，避免重复登录。
    * 自动填写账号、密码，并根据配置选择正确的运营商。
    * 自动点击登录按钮，提交认证表单。
    * **可被计划**：该脚本可以被设置为开机自启动实现全自动登录。

## 第二部分：部署文档

我们提供两种使用方式：直接运行打包好的程序（推荐）或自行从源码部署。

### 1. 使用已打包的 EXE 文件（推荐）

对于大多数用户，我们建议直接从 Release 页面下载打包好的可执行文件，这是最简单快捷的方式。

* **下载**：请前往本仓库的 **[Releases](https://github.com/sep-zxy/Auto-login-on-campus-network/releases)** 页面，下载最新的压缩包。解压后按发行包提供的配置入口和登录入口运行，具体文件名以实际发行内容为准。

* **步骤一：配置你的登录信息**
    1.  打开发行包中的配置工具。
    2.  在弹出的窗口中，输入你的校园网 **账号** 和 **密码**。
    3.  **运营商 / 认证域** 必须填写登录页面选项框中实际显示的完整文本；配置界面的默认示例值需要按目标页面核对。
    4.  点击 **“保存配置”** 按钮。程序会提示保存成功，并在同目录下生成一个 `config.json` 文件。

* **步骤二：执行登录**
    1.  运行发行包中的自动登录程序。
    2.  程序在后台执行页面流程；检测为已在线时跳过提交，否则填写并提交表单，执行结束后退出。请以 Portal 状态或实际访问结果确认是否联网。

* **（可选）步骤三：设置开机自启动**
    可以通过 Windows 启动文件夹或任务计划程序启动登录程序，并将工作目录设为程序和配置文件所在目录。若发行包附带启动管理脚本，可按包内说明设置。
   
### 2. 自行部署运行（适合开发者）

如果你想从源代码运行、修改或调试本项目，请遵循以下步骤。

* **环境要求**
    * Python 环境（以下源码示例通过 uv 使用 Python 3.12）
    * AutoHotkey v2.0+

* **步骤一：克隆或下载仓库**
    ```powershell
    $ErrorActionPreference = 'Stop'
    git clone 'https://github.com/sep-zxy/Auto-login-on-campus-network.git'
    Set-Location 'Auto-login-on-campus-network'
    ```

* **步骤二：准备 Python 依赖与浏览器**
    使用 uv 为运行命令准备 Playwright；浏览器通道固定为 `msedge`，默认使用 Microsoft Edge。
    ```powershell
    $ErrorActionPreference = 'Stop'
    uv run --python 3.12 --with playwright python -m playwright install msedge
    ```
    Playwright 安装方式与系统要求见 [官方文档](https://playwright.dev/python/docs/intro)。

* **步骤三：配置登录信息**
    你有两种方式来创建 `config.json` 配置文件：
    1.  **使用 AHK 工具**：直接运行仓库中的 `.ahk` 脚本，填写信息并保存。
    2.  **手动创建**：在项目根目录下手动创建一个名为 `config.json` 的文件，并填入以下内容（请替换为你的真实信息）：
        ```json
        {
          "username": "你的学号",
          "password": "你的密码",
          "operator_label": "认证页面显示的运营商名称"
        }
        ```
        *注意：`operator_label` 必须与登录页面下拉菜单中的文本完全一致。`config.json` 中的账号和密码为明文，本地配置未加密。*

* **步骤四：运行登录脚本**
    打开终端或命令行，确保你在项目根目录下，然后执行：
    ```powershell
    $ErrorActionPreference = 'Stop'
    uv run --python 3.12 --with playwright python './autologin.py'
    ```
    请在仓库目录运行，以读取同目录下的 `config.json`。

脚本读取 `config.json` 后执行页面流程，输出已在线、提交完成或异常提示。实际联网结果需结合 Portal 状态确认。
