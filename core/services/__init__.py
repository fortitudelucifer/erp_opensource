# -*- coding: utf-8 -*-
"""
service 层初始化模块。
- 把复杂的业务逻辑从视图（blueprint）中抽离出来
"""

# core/services/__init__.py

from .notification_service import (
    NotificationService,
    NotificationChannel,
    DummyNotificationService,
    get_notification_service,  # 新增
)

