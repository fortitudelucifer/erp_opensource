# -*- coding: utf-8 -*-
"""
feedback_service.py - 售后反馈服务模块 / Feedback Service Module

本模块封装客户反馈相关的业务逻辑：
This module encapsulates the business logic for customer feedback:

- get_summary_for_contract: 获取合同反馈统计 / Get feedback summary for contract

Feedback Status / 反馈状态:
未解决 → 已解决
Unresolved → Resolved

Author: fortitudelucifer (https://github.com/fortitudelucifer)
License: Apache-2.0
"""

from __future__ import annotations

from typing import Dict, Any

from flask_sqlalchemy import SQLAlchemy

from ..models import Feedback, Contract



class FeedbackService:
    """客户反馈相关业务服务。

    当前主要职责：
        - 为单个合同提供反馈统计信息：
          * 总反馈条数
          * 未解决条数
          * 已解决条数
    """

    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def get_summary_for_contract(self, contract: Contract) -> Dict[str, Any]:
        """获取指定合同的反馈统计信息。

        返回的字典示例：
            {
                "total": 4,
                "resolved": 3,
                "unresolved": 1,
            }
        """
        q = Feedback.query.filter_by(contract_id=contract.id)
        records = q.all()

        total = len(records)
        unresolved = sum(1 for fb in records if not getattr(fb, "is_resolved", False))
        resolved = total - unresolved

        return {
            "total": total,
            "resolved": resolved,
            "unresolved": unresolved,
        }
