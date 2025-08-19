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

        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)

        username = config['username']
        password = config['password']

        # 从配置中读取运营商标签，如果不存在，则默认为 '巢湖学院'
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

            # 检查是否已登录
            try:
                page.locator("#logout").wait_for(state="visible", timeout=3000)
                browser.close()
                return
            except PlaywrightTimeoutError:
                pass  # 未登录，继续执行

            # 执行登录操作
            page.locator("#username").fill(username)
            page.locator("#password").fill(password)
            page.select_option("#domain", label=operator_label)
            page.locator("#login-account").click()

            page.wait_for_timeout(5000)

        except Exception as e:
            print(f"脚本执行时发生错误: {e}")
        finally:
            if browser and not browser.is_closed():
                browser.close()


if __name__ == "__main__":
    run_login()