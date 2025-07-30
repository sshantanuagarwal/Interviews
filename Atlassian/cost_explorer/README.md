# Cost Explorer System

A comprehensive system for calculating and analyzing customer costs on a monthly and yearly basis, designed for the payments team.

## 🏗️ Architecture Overview

The Cost Explorer system follows a clean architecture pattern with clear separation of concerns:

```
cost_explorer/
├── models.py          # Data models and entities
├── repository.py      # Data access layer (abstract + concrete implementations)
├── services.py        # Business logic layer
├── presenters.py      # Presentation and formatting layer
├── __init__.py        # Package initialization
├── example_usage.py   # Comprehensive usage examples
└── README.md          # This file
```

## 🎯 Key Features

### 💰 Cost Calculation
- **Monthly Cost Calculation**: Calculate costs for any specific month
- **Yearly Cost Calculation**: Calculate costs for any specific year
- **Custom Period Calculation**: Calculate costs for custom date ranges
- **Transaction Type Breakdown**: Separate costs by payment, fee, refund, etc.

### 📊 Reporting
- **Customer Cost Reports**: Comprehensive reports for individual customers
- **Aggregate Reports**: Company-wide cost summaries
- **Multi-Year Analysis**: Track costs across multiple years
- **Top Customer Rankings**: Identify highest-value customers

### 📈 Analysis
- **Cost Trends**: Analyze growth patterns over time
- **Anomaly Detection**: Identify unusual cost patterns using statistical analysis
- **Seasonal Patterns**: Understand monthly cost variations
- **Growth Rate Calculation**: Measure year-over-year growth

### 📤 Export Capabilities
- **CSV Export**: Generate reports in CSV format
- **JSON Export**: Export data in structured JSON format
- **Tabular Display**: Beautiful formatted tables using tabulate

## 🚀 Quick Start

### Installation

```bash
# Install required dependencies
pip install tabulate
```

### Basic Usage

```python
from cost_explorer import (
    FileBasedCustomerRepository, FileBasedTransactionRepository,
    CostCalculationService, CostReportingService
)

# Create repositories
customer_repo = FileBasedCustomerRepository('customers.json')
transaction_repo = FileBasedTransactionRepository('transactions.json')

# Create services
cost_service = CostCalculationService(customer_repo, transaction_repo)
reporting_service = CostReportingService(cost_service)

# Calculate monthly costs
monthly_cost = cost_service.calculate_monthly_costs("CUST001", 2024, 6)

# Generate comprehensive report
report = reporting_service.generate_customer_cost_report("CUST001", 2024)
```

### Run the Example

```bash
cd cost_explorer
python example_usage.py
```

## 📋 Data Models

### Customer
```python
@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    billing_cycle: BillingCycle  # monthly, yearly, quarterly, weekly
    created_date: datetime
    is_active: bool = True
    metadata: Dict[str, Any] = None
```

### Transaction
```python
@dataclass
class Transaction:
    transaction_id: str
    customer_id: str
    amount: Decimal
    currency: str
    transaction_type: TransactionType  # payment, refund, fee, discount, tax
    transaction_date: datetime
    description: str
    reference_id: Optional[str] = None
    metadata: Dict[str, Any] = None
```

### Cost Summary
```python
@dataclass
class CostSummary:
    customer_id: str
    period_start: date
    period_end: date
    total_amount: Decimal
    currency: str
    transaction_count: int
    breakdown: Dict[TransactionType, Decimal]
    metadata: Dict[str, Any] = None
```

## 🔧 Services

### CostCalculationService
- `calculate_monthly_costs(customer_id, year, month)`
- `calculate_yearly_costs(customer_id, year)`
- `calculate_custom_period_costs(customer_id, start_date, end_date)`

### CostReportingService
- `generate_customer_cost_report(customer_id, year)`
- `generate_multi_year_report(customer_id, start_year, end_year)`
- `generate_aggregate_report(year)`

### CostAnalysisService
- `analyze_cost_trends(customer_id, start_year, end_year)`
- `identify_cost_anomalies(customer_id, year, threshold)`

## 📊 Report Examples

### Customer Cost Report
```
================================================================================
💰 CUSTOMER COST REPORT - ACME CORPORATION 💰
================================================================================
Customer ID: CUST001
Email: billing@acme.com
Billing Cycle: monthly
Report Generated: 2024-01-15 10:30:00

📊 SUMMARY
----------------------------------------
+------------------------+------------------+
| Metric                 | Value            |
+========================+==================+
| Total Yearly Amount    | USD 78,000.00   |
+------------------------+------------------+
| Average Monthly Amount | USD 6,500.00    |
+------------------------+------------------+
| Average Yearly Amount  | USD 78,000.00   |
+------------------------+------------------+
| Total Monthly Amount   | USD 78,000.00   |
+------------------------+------------------+
```

### Aggregate Report
```
================================================================================
🏢 AGGREGATE COST REPORT - 2024 🏢
================================================================================
Total Customers: 3
Total Revenue: 123,000.00

🏆 TOP CUSTOMERS
----------------------------------------
+------+------------------+------------+----------------+------------------+
| Rank | Customer Name    | Customer ID| Yearly Total   | Avg Monthly      |
+======+==================+============+================+==================+
|    1 | Acme Corporation | CUST001    | USD 78,000.00 | USD 6,500.00    |
+------+------------------+------------+----------------+------------------+
|    2 | Global Industries| CUST002    | USD 60,000.00 | USD 5,000.00    |
+------+------------------+------------+----------------+------------------+
|    3 | Startup Inc      | CUST003    | USD 5,400.00  | USD 450.00      |
+------+------------------+------------+----------------+------------------+
```

## 🔄 Repository Pattern

The system uses the Repository pattern for data access:

```python
# Abstract base classes
class CustomerRepository(ABC):
    @abstractmethod
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        pass

class TransactionRepository(ABC):
    @abstractmethod
    def get_transactions_by_customer(self, customer_id: str, 
                                   start_date: Optional[date] = None,
                                   end_date: Optional[date] = None) -> List[Transaction]:
        pass

# Concrete implementations
class FileBasedCustomerRepository(CustomerRepository):
    # JSON file-based implementation

class FileBasedTransactionRepository(TransactionRepository):
    # JSON file-based implementation
```

## 📈 Analysis Features

### Cost Trends Analysis
- Year-over-year growth calculation
- Monthly average patterns
- Seasonal trend identification
- Growth rate percentage

### Anomaly Detection
- Statistical analysis using Z-scores
- Configurable threshold for anomaly detection
- Expected range calculation
- Unusual cost pattern identification

## 🎨 Design Patterns Used

1. **Repository Pattern**: Abstract data access layer
2. **Service Layer Pattern**: Business logic separation
3. **Presenter Pattern**: Formatting and display logic
4. **Strategy Pattern**: Different export formats
5. **Factory Pattern**: Service creation
6. **Observer Pattern**: Event-driven reporting

## 🔒 Data Integrity

- **Decimal Precision**: All monetary calculations use `Decimal` for accuracy
- **Type Safety**: Full type hints throughout the codebase
- **Data Validation**: Input validation and error handling
- **Immutable Data**: Dataclasses for data integrity

## 🚀 Performance Considerations

- **Lazy Loading**: Data loaded only when needed
- **Caching**: Repository-level caching for frequently accessed data
- **Efficient Queries**: Optimized date range filtering
- **Memory Management**: Proper cleanup of large datasets

## 📝 Usage Examples

### Simple Monthly Calculation
```python
# Calculate costs for June 2024
monthly_cost = cost_service.calculate_monthly_costs("CUST001", 2024, 6)
print(f"June 2024 costs: ${monthly_cost.total_amount:,.2f}")
```

### Comprehensive Report Generation
```python
# Generate full customer report
report = reporting_service.generate_customer_cost_report("CUST001", 2024)
presenter = CostReportPresenter()
formatted_report = presenter.format_customer_cost_report(report)
print(formatted_report)
```

### Export to File
```python
# Export to CSV
exporter = CostReportExporter(presenter)
exporter.export_to_csv(report, "customer_report.csv")
exporter.export_to_json(report, "customer_report.json")
```

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Add comprehensive type hints
3. Include docstrings for all public methods
4. Write unit tests for new features
5. Update documentation as needed

## 📄 License

This project is designed for internal use by the payments team. 