from typing import List, Literal
from pydantic import BaseModel, Field

class ApplicantInput(BaseModel):
    age: int = Field(..., ge=18, le=100, example=35)
    education: Literal["Graduate", "High School", "Postgraduate"] = Field(..., example="Graduate")
    home_ownership: Literal["Mortgage", "Own", "Rent"] = Field(..., example="Mortgage")
    employment_years: float = Field(..., ge=0, example=8.0)
    annual_income: float = Field(..., gt=0, example=750000.0)
    total_debt: float = Field(..., ge=0, example=150000.0)
    num_credit_cards: int = Field(..., ge=0, example=3)
    existing_loans: int = Field(..., ge=0, example=1)
    credit_utilization: float = Field(..., ge=0.0, le=1.0, example=0.25)
    credit_history_years: float = Field(..., ge=0, example=10.0)
    late_payments_12m: int = Field(..., ge=0, example=0)
    missed_payments_total: int = Field(..., ge=0, example=1)
    loan_amount: float = Field(..., gt=0, example=200000.0)
    loan_term_months: int = Field(..., example=36)

class AssessmentResponse(BaseModel):
    verdict: str
    is_creditworthy: bool
    risk_score_pct: float
    debt_to_income: float
    loan_to_income: float
    risk_level: str
    key_factors: List[str]
