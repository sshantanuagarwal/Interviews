"""
Cost Explorer - A comprehensive system for calculating and analyzing customer costs.

This package provides a complete solution for the payments team to calculate
customer costs on a monthly and yearly basis with advanced reporting capabilities.
"""

from .models import (
    Customer, Transaction, CostSummary, CustomerCostReport,
    TransactionType, BillingCycle
)
from .repository import (
    CustomerRepository, TransactionRepository,
    FileBasedCustomerRepository, FileBasedTransactionRepository
)
from .services import (
    CostCalculationService, CostReportingService, CostAnalysisService
)
from .presenters import CostReportPresenter, CostReportExporter

__version__ = "1.0.0"
__author__ = "Payments Team"

__all__ = [
    # Models
    'Customer', 'Transaction', 'CostSummary', 'CustomerCostReport',
    'TransactionType', 'BillingCycle',
    
    # Repositories
    'CustomerRepository', 'TransactionRepository',
    'FileBasedCustomerRepository', 'FileBasedTransactionRepository',
    
    # Services
    'CostCalculationService', 'CostReportingService', 'CostAnalysisService',
    
    # Presenters
    'CostReportPresenter', 'CostReportExporter'
] 