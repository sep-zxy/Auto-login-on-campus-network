import os
import json
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

CONFIG_FILE = 'config.json'


def run_login():
    """读取配置并执行静默登录 (同步模式)"""
    try:
        if not os.path.exists(CONFIG_FILE):
            print(f"配置文件 {CONFIG_FILE} 不存在，已跳过登录。")
            return

        # *** 核心修正：将 'utf-8' 修改为 'utf-8-sig' 来处理 BOM ***
        with open(CONFIG_FILE, 'r', encoding='utf-8-sig') as f:
            config = json.load(f)

        username = config['username']
        password = config['password']
        operator_label = config.get('operator_label', '巢湖学院')

    except Exception as e:
        print(f"读取配置文件时发生错误: {e}")
        return

    with sync_playwright() as p:
        browser = None
        try:
            browser = p.chromium.launch(channel="msedge", headless=True)
            page = browser.new_page()
            page.goto("http://210.45.92.67/")

            try:
                # If logout button is visible, we're already logged in.
                page.locator("#logout").wait_for(state="visible", timeout=3000)
                print("已经登录，无需重复操作。")
                browser.close()
                return
            except PlaywrightTimeoutError:
                # Not logged in, continue with login process.
                pass

            page.locator("#username").fill(username)
            page.locator("#password").fill(password)
            page.select_option("#domain", label=operator_label)
            page.locator("#login-account").click()

            print("登录成功！")
            # A hard wait is okay for a simple script, but waiting for a specific element
            # that confirms login is more robust.
            page.wait_for_timeout(5000)

        except Exception as e:
            print(f"脚本执行时发生错误: {e}")
        finally:
            # *** THIS IS THE CORRECTED LINE ***
            if browser and browser.is_connected():
                browser.close()


if __name__ == "__main__":
    run_login()

