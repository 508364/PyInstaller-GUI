# -*- coding: utf-8 -*-
import importlib
import locale
import os
import sys

_LANG_MODULES = {
    "zh_CN": "i18n.zh_CN",
    "zh_TW": "i18n.zh_TW",
    "en_US": "i18n.en_US",
}

def _normalize(lang: str) -> str:
    s = (lang or "").lower().replace("-", "_")
    # 常见中文区域与关键词判断
    if any(x in s for x in ("zh_tw", "zh_hk", "taiwan", "hong_kong")):
        return "zh_TW"
    if s.startswith("zh") or "chinese" in s or "china" in s or "zh_cn" in s or "chs" in s:
        return "zh_CN"
    return "en_US"

def detect_language_code() -> str:
    # 允许环境变量强制语言（可选）
    env_lang = os.environ.get("PI_GUI_LANG")
    if env_lang:
        return _normalize(env_lang)

    # 尝试使用系统本地化（不使用已弃用的 getdefaultlocale）
    try:
        locale.setlocale(locale.LC_ALL, "")
    except Exception:
        pass

    lang = None

    # 方案1：locale.getlocale（未弃用）
    try:
        lang = (locale.getlocale() or (None, None))[0]
    except Exception:
        lang = None

    # 方案2：Windows 下使用用户界面语言 ID（区分简体/繁体）
    if not lang and sys.platform.startswith("win"):
        try:
            import ctypes
            lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            if lcid in (0x0804, 0x1004, 0x2004):  # 简中：大陆/新加坡/澳门(简)
                return "zh_CN"
            if lcid in (0x0404, 0x0C04, 0x1404):  # 繁中：台湾/香港/澳门(繁)
                return "zh_TW"
        except Exception:
            pass

    # 方案3：环境变量
    if not lang:
        for env in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
            val = os.environ.get(env)
            if val:
                lang = val
                break

    return _normalize(lang)

def get_translator(lang_code: str):
    # 兼容脚本运行与 PyInstaller 打包后的路径
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    # 确保 i18n 包所在的上级目录可被导入
    pkg_root = os.path.dirname(base_dir) if os.path.basename(base_dir) == "i18n" else os.path.dirname(os.path.abspath(__file__))
    if pkg_root and pkg_root not in sys.path:
        sys.path.insert(0, pkg_root)

    module_name = _LANG_MODULES.get(lang_code, _LANG_MODULES["en_US"])
    try:
        mod = importlib.import_module(module_name)
    except Exception:
        # 回退英文
        try:
            mod = importlib.import_module(_LANG_MODULES["en_US"])
        except Exception:
            # 最后兜底：返回 key 自身
            class _Dummy: STRINGS = {}
            mod = _Dummy()

    STRINGS = getattr(mod, "STRINGS", {})

    def _t(key: str, **kwargs):
        text = STRINGS.get(key, key)
        try:
            return text.format(**kwargs) if kwargs else text
        except Exception:
            return text
    return _t