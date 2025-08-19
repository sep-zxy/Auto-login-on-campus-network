import tkinter as tk
from tkinter import messagebox
import json
import os

CONFIG_FILE = 'config.json'


class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("登录信息配置")
        # 增加窗口高度以容纳新的一行
        self.root.geometry("400x220")

        main_frame = tk.Frame(root, padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text="账号:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.username_entry = tk.Entry(main_frame, width=35)
        self.username_entry.grid(row=0, column=1, padx=5, pady=8)

        tk.Label(main_frame, text="密码:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.password_entry = tk.Entry(main_frame, show="*", width=35)
        self.password_entry.grid(row=1, column=1, padx=5, pady=8)

        # --- 新增部分 ---
        tk.Label(main_frame, text="运营商:").grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.operator_entry = tk.Entry(main_frame, width=35)
        self.operator_entry.grid(row=2, column=1, padx=5, pady=8)
        # ----------------

        save_button = tk.Button(main_frame, text="💾 保存配置", command=self.save_config, font=("Helvetica", 10, "bold"))
        save_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.load_config()

    def save_config(self):
        """获取所有输入，并以JSON格式保存到文件"""
        config_data = {
            'username': self.username_entry.get(),
            'password': self.password_entry.get(),
            # 保存运营商标签
            'operator_label': self.operator_entry.get()
        }

        if not all(config_data.values()):  # 检查所有值是否都非空
            messagebox.showwarning("输入错误", "所有字段均不能为空！")
            return

        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)
            messagebox.showinfo("成功", f"配置已成功保存到 {CONFIG_FILE}")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")

    def load_config(self):
        """尝试加载现有的JSON配置文件到输入框"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)

                self.username_entry.insert(0, config_data.get('username', ''))
                self.password_entry.insert(0, config_data.get('password', ''))
                # 加载运营商标签，如果不存在则默认为 '巢湖学院'
                self.operator_entry.insert(0, config_data.get('operator_label', '巢湖学院'))
            except Exception:
                # 如果加载失败，仍提供一个默认值
                self.operator_entry.insert(0, '巢湖学院')
        else:
            # 如果配置文件不存在，提供一个默认值
            self.operator_entry.insert(0, '巢湖学院')


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigApp(root)
    root.mainloop()