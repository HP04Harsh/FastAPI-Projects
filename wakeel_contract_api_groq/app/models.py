from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ContractStatus(str, Enum):
    UPLOADED = "UPLOADED"
    IN_PROGRESS = "IN_PROGRESS"
    ANALYZED = "ANALYZED"
    FAILED = "FAILED"


class ContractBase(BaseModel):
    file_name: str
    original_file_name: str
    upload_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    page_count: int
    word_count: int
    status: ContractStatus = ContractStatus.UPLOADED


class ContractCreate(ContractBase):
    text_content: str


class ContractRead(ContractBase):
    id: str


class ClauseAnalysis(BaseModel):
    clause_title: str
    clause_text: str
    explanation: str


class RiskFlag(BaseModel):
    title: str
    description: str
    risk_level: RiskLevel


class AnalysisResult(BaseModel):
    id: Optional[str] = None
    contract_id: str
    analysis_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    summary: str
    contract_type: str
    key_clauses: List[ClauseAnalysis]
    risk_flags: List[RiskFlag]
    overall_risk_level: RiskLevel
    recommendations: List[str]