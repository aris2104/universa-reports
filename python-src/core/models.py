from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReportModel:
    title: str
    type_report: str
    author: str = ""
