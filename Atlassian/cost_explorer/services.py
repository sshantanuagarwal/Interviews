from typing import List, Dict, Optional, Any
from datetime import datetime, date, timedelta
from decimal import Decimal
from collections import defaultdict
import calendar

from models import Customer, Transaction, CostSummary, CustomerCostReport,    TransactionType, BillingCycle
from repository import CustomerRepository, TransactionRepository


class CostCalculationService:
    """Service for calculating customer costs."""
    
    def __init__(self, customer_repo: CustomerRepository, transaction_repo: TransactionRepository):
        self.customer_repo = customer_repo
        self.transaction_repo = transaction_repo
    
    def calculate_monthly_costs(self, customer_id: str, year: int, month: int) -> CostSummary:
        """Calculate costs for a specific month."""
        start_date = date(year, month, 1)
        end_date = date(year, month, calendar.monthrange(year, month)[1])
        
        transactions = self.transaction_repo.get_transactions_by_customer(
            customer_id, start_date, end_date
        )
        
        return self._create_cost_summary(customer_id, start_date, end_date, transactions)
    
    def calculate_yearly_costs(self, customer_id: str, year: int) -> CostSummary:
        """Calculate costs for a specific year."""
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        
        transactions = self.transaction_repo.get_transactions_by_customer(
            customer_id, start_date, end_date
        )
        
        return self._create_cost_summary(customer_id, start_date, end_date, transactions)
    
    def calculate_custom_period_costs(self, customer_id: str, start_date: date, end_date: date) -> CostSummary:
        """Calculate costs for a custom date period."""
        transactions = self.transaction_repo.get_transactions_by_customer(
            customer_id, start_date, end_date
        )
        
        return self._create_cost_summary(customer_id, start_date, end_date, transactions)
    
    def _create_cost_summary(self, customer_id: str, start_date: date, end_date: date, 
                           transactions: List[Transaction]) -> CostSummary:
        """Create a cost summary from transactions."""
        if not transactions:
            return CostSummary(
                customer_id=customer_id,
                period_start=start_date,
                period_end=end_date,
                total_amount=Decimal('0'),
                currency='USD',
                transaction_count=0,
                breakdown={}
            )
        
        # Group transactions by type
        breakdown = defaultdict(Decimal)
        total_amount = Decimal('0')
        
        for transaction in transactions:
            breakdown[transaction.transaction_type] += transaction.amount
            total_amount += transaction.amount
        
        # Use currency from first transaction
        currency = transactions[0].currency
        
        return CostSummary(
            customer_id=customer_id,
            period_start=start_date,
            period_end=end_date,
            total_amount=total_amount,
            currency=currency,
            transaction_count=len(transactions),
            breakdown=dict(breakdown)
        )


class CostReportingService:
    """Service for generating comprehensive cost reports."""
    
    def __init__(self, cost_calculation_service: CostCalculationService):
        self.cost_calculation_service = cost_calculation_service
    
    def generate_customer_cost_report(self, customer_id: str, year: int) -> CustomerCostReport:
        """Generate a comprehensive cost report for a customer for a specific year."""
        customer = self.cost_calculation_service.customer_repo.get_customer(customer_id)
        if not customer:
            raise ValueError(f"Customer {customer_id} not found")
        
        # Calculate monthly costs
        monthly_costs = []
        for month in range(1, 13):
            monthly_cost = self.cost_calculation_service.calculate_monthly_costs(
                customer_id, year, month
            )
            monthly_costs.append(monthly_cost)
        
        # Calculate yearly cost
        yearly_cost = self.cost_calculation_service.calculate_yearly_costs(customer_id, year)
        
        # Calculate totals and averages
        total_monthly_amount = sum(cost.total_amount for cost in monthly_costs)
        total_yearly_amount = yearly_cost.total_amount
        
        # Calculate averages (excluding months with no transactions)
        active_months = [cost for cost in monthly_costs if cost.transaction_count > 0]
        average_monthly_amount = (
            sum(cost.total_amount for cost in active_months) / len(active_months)
            if active_months else Decimal('0')
        )
        
        average_yearly_amount = total_yearly_amount / 12 if total_yearly_amount > 0 else Decimal('0')
        
        return CustomerCostReport(
            customer=customer,
            monthly_costs=monthly_costs,
            yearly_costs=[yearly_cost],
            total_monthly_amount=total_monthly_amount,
            total_yearly_amount=total_yearly_amount,
            average_monthly_amount=average_monthly_amount,
            average_yearly_amount=average_yearly_amount,
            currency=yearly_cost.currency,
            generated_date=datetime.now()
        )
    
    def generate_multi_year_report(self, customer_id: str, start_year: int, end_year: int) -> List[CustomerCostReport]:
        """Generate cost reports for multiple years."""
        reports = []
        for year in range(start_year, end_year + 1):
            try:
                report = self.generate_customer_cost_report(customer_id, year)
                reports.append(report)
            except ValueError:
                # Skip years where customer doesn't exist
                continue
        return reports
    
    def generate_aggregate_report(self, year: int) -> Dict[str, Any]:
        """Generate aggregate report for all customers in a year."""
        customers = self.cost_calculation_service.customer_repo.get_all_customers()
        
        aggregate_data = {
            'year': year,
            'total_customers': len(customers),
            'total_revenue': Decimal('0'),
            'customer_reports': [],
            'top_customers': [],
            'monthly_totals': [Decimal('0') for _ in range(12)]
        }
        
        customer_reports = []
        for customer in customers:
            try:
                report = self.generate_customer_cost_report(customer.customer_id, year)
                customer_reports.append(report)
                aggregate_data['total_revenue'] += report.total_yearly_amount
                
                # Add to monthly totals
                for i, monthly_cost in enumerate(report.monthly_costs):
                    aggregate_data['monthly_totals'][i] += monthly_cost.total_amount
                    
            except ValueError:
                continue
        
        # Sort by total yearly amount to get top customers
        customer_reports.sort(key=lambda x: x.total_yearly_amount, reverse=True)
        aggregate_data['customer_reports'] = customer_reports
        aggregate_data['top_customers'] = customer_reports[:10]  # Top 10 customers
        
        return aggregate_data


class CostAnalysisService:
    """Service for advanced cost analysis and insights."""
    
    def __init__(self, cost_calculation_service: CostCalculationService):
        self.cost_calculation_service = cost_calculation_service
    
    def analyze_cost_trends(self, customer_id: str, start_year: int, end_year: int) -> Dict[str, Any]:
        """Analyze cost trends over multiple years."""
        trends = {
            'customer_id': customer_id,
            'years': [],
            'yearly_totals': [],
            'monthly_averages': [],
            'growth_rate': None,
            'seasonal_patterns': {}
        }
        
        yearly_costs = []
        for year in range(start_year, end_year + 1):
            try:
                yearly_cost = self.cost_calculation_service.calculate_yearly_costs(customer_id, year)
                yearly_costs.append((year, yearly_cost))
                trends['years'].append(year)
                trends['yearly_totals'].append(float(yearly_cost.total_amount))
            except ValueError:
                continue
        
        if len(yearly_costs) >= 2:
            # Calculate growth rate
            first_year_amount = yearly_costs[0][1].total_amount
            last_year_amount = yearly_costs[-1][1].total_amount
            
            if first_year_amount > 0:
                growth_rate = ((last_year_amount - first_year_amount) / first_year_amount) * 100
                trends['growth_rate'] = float(growth_rate)
        
        # Calculate monthly averages across all years
        monthly_totals = [Decimal('0') for _ in range(12)]
        month_counts = [0 for _ in range(12)]
        
        for year, yearly_cost in yearly_costs:
            for i, monthly_cost in enumerate(yearly_cost.breakdown.values()):
                monthly_totals[i] += monthly_cost
                month_counts[i] += 1
        
        trends['monthly_averages'] = [
            float(monthly_totals[i] / month_counts[i]) if month_counts[i] > 0 else 0
            for i in range(12)
        ]
        
        return trends
    
    def identify_cost_anomalies(self, customer_id: str, year: int, threshold: float = 2.0) -> List[Dict[str, Any]]:
        """Identify unusual cost patterns."""
        monthly_costs = []
        for month in range(1, 13):
            cost = self.cost_calculation_service.calculate_monthly_costs(customer_id, year, month)
            monthly_costs.append((month, cost))
        
        # Calculate statistics
        amounts = [float(cost.total_amount) for _, cost in monthly_costs if cost.transaction_count > 0]
        if not amounts:
            return []
        
        mean_amount = sum(amounts) / len(amounts)
        variance = sum((amount - mean_amount) ** 2 for amount in amounts) / len(amounts)
        std_dev = variance ** 0.5
        
        anomalies = []
        for month, cost in monthly_costs:
            if cost.transaction_count > 0:
                cost_amount = float(cost.total_amount)
                z_score = abs(cost_amount - mean_amount) / std_dev if std_dev > 0 else 0
                if z_score > threshold:
                    anomalies.append({
                        'month': month,
                        'amount': cost_amount,
                        'z_score': z_score,
                        'expected_range': (float(mean_amount - threshold * std_dev), 
                                         float(mean_amount + threshold * std_dev))
                    })
        
        return anomalies 