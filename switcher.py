import pyautogui
import time
import subprocess
import sys


def emergency_switch():
    """
    执行应急切换动作。
    方案：直接新建并切换到全新的虚拟桌面（Windows 10/11 支持）。
    """
    try:
        # 快捷键：Ctrl + Win + D = 新建虚拟桌面并立即切换过去
        pyautogui.hotkey('ctrl', 'win', 'd')
        print("[Switcher] 已切换到新建的虚拟桌面（工作伪装模式）")

        # 可选：自动静音，防止视频声音暴露
        pyautogui.press('volumemute')
        print("[Switcher] 已静音")

        # 极短暂停确保快捷键生效
        time.sleep(0.1)
    except Exception as e:
        print(f"[Switcher] 切换失败: {e}")


def switch_to_app(app_keyword="Visual Studio Code"):
    """
    备选方案：切换到指定应用程序窗口（例如 VS Code）。
    需要安装 pygetwindow: pip install pygetwindow
    """
    try:
        import pygetwindow as gw
        # 查找标题包含关键词的窗口
        windows = gw.getWindowsWithTitle(app_keyword)
        if windows:
            win = windows[0]
            win.activate()
            print(f"[Switcher] 已切换到窗口: {win.title}")
        else:
            # 如果没找到目标窗口，回退到虚拟桌面方案
            print(f"[Switcher] 未找到包含 '{app_keyword}' 的窗口，使用虚拟桌面")
            emergency_switch()
    except ImportError:
        print("[Switcher] pygetwindow 未安装，使用虚拟桌面方案")
        emergency_switch()