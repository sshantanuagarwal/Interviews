from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Dict, Any
from enum import Enum


class TransactionType(Enum):
    """Types of transactions that can occur."""
    PAYMENT = "payment"
    REFUND = "refund"
    FEE = "fee"
    DISCOUNT = "discount"
    TAX = "tax"


class BillingCycle(Enum):
    """Billing cycle types."""
    MONTHLY = "monthly"
    YEARLY = "yearly"
    QUARTERLY = "quarterly"
    WEEKLY = "weekly"


@dataclass
class Customer:
    """Customer entity with billing information."""
    customer_id: str
    name: str
    email: str
    billing_cycle: BillingCycle
    created_date: datetime
    is_active: bool = True
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Transaction:
    """Individual transaction record."""
    transaction_id: str
    customer_id: str
    amount: Decimal
    currency: str
    transaction_type: TransactionType
    transaction_date: datetime
    description: str
    reference_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CostSummary:
    """Summary of costs for a specific period."""
    customer_id: str
    period_start: date
    period_end: date
    total_amount: Decimal
    currency: str
    transaction_count: int
    breakdown: Dict[TransactionType, Decimal]
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CustomerCostReport:
    """Complete cost report for a customer."""
    customer: Customer
    monthly_costs: List[CostSummary]
    yearly_costs: List[CostSummary]
    total_monthly_amount: Decimal
    total_yearly_amount: Decimal
    average_monthly_amount: Decimal
    average_yearly_amount: Decimal
    currency: str
    generated_date: datetime 