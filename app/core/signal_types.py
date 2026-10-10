
from enum import Enum


class SignalType(str, Enum):
    HIRING = "hiring"
    FUNDING = "funding"
    LEADERSHIP_CHANGE = "leadership_change"
    EXPANSION = "expansion"
    TECHNOLOGY_CHANGE = "technology_change"
    WEBSITE_CHANGE = "website_change"
    INTENT = "intent"
    JOB_CHANGE = "job_change"
    COMPANY_GROWTH = "company_growth"
    OTHER = "other"


SIGNAL_STRENGTH = {
    SignalType.HIRING: 60,
    SignalType.FUNDING: 80,
    SignalType.LEADERSHIP_CHANGE: 75,
    SignalType.EXPANSION: 70,
    SignalType.TECHNOLOGY_CHANGE: 65,
    SignalType.WEBSITE_CHANGE: 40,
    SignalType.INTENT: 90,
    SignalType.JOB_CHANGE: 55,
    SignalType.COMPANY_GROWTH: 70,
    SignalType.OTHER: 30,
}
