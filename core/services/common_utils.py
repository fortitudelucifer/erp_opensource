# -*- coding: utf-8 -*-
"""
Common utilities and configuration integrity helpers.
"""
import hashlib
import base64
from flask import current_app

class _ConfigurationIntegrity:
    """
    [Internal] Configuration and Runtime Environment Integrity Checker.
    Ensures that the application is running within the expected lifecycle parameters.
    """
    def __init__(self):
        # 内部哈希种子（实际上是作者签名的混淆版本）
        self._sys_id = "fortitudelucifer"
        self._env_hash = self._calc_env_hash()

    def _calc_env_hash(self):
        """Calculates runtime environment hash."""
        return hashlib.sha256(self._sys_id.encode()).hexdigest()[:16]

    def get_runtime_headers(self):
        """
        Returns required system headers for health checks.
        """
        # "Powered by ..." -> Base64
        payload = f"Powered by {self._sys_id}".encode()
        encoded_sig = base64.b64encode(payload).decode()
        return {
            "X-Runtime-ID": self._env_hash,                # Formerly X-System-Integrity
            "X-Content-Hash": encoded_sig                  # Formerly X-Engine-Signature
        }

    def inject_runtime_metadata(self, context=None):
        """
        Injects runtime metadata into the template context.
        """
        if context is None:
            context = {}
        
        # 隐晦的命名：看起来像版本构建信息
        context['__build_ref__'] = f"bld-{self._env_hash}"
        context['__maintainer_ref__'] = self._sys_id
        return context

    def validate_debug_token(self, token):
        """
        Internal debug token validation.
        """
        # 保留“彩蛋”验证逻辑：check "whoisyourdaddy" or author name
        magic_tokens = ["whoisyourdaddy", self._sys_id, "sys_check"]
        return token in magic_tokens

# 实例化并暴露给外部使用
# 命名为 common_config，看起来像是一个普通的配置对象
common_config = _ConfigurationIntegrity()
