#!/usr/bin/env python3
"""
Example usage of the Cost Explorer system.

This script demonstrates how to use the cost explorer to calculate
customer costs on a monthly and yearly basis.
"""

import os
from datetime import datetime, date
from decimal import Decimal
import uuid

from cost_explorer import (
    Customer, Transaction, TransactionType, BillingCycle,
    FileBasedCustomerRepository, FileBasedTransactionRepository,
    CostCalculationService, CostReportingService, CostAnalysisService,
    CostReportPresenter, CostReportExporter
)


def create_sample_data():
    """Create sample customer and transaction data."""
    
    # Create repositories
    customer_repo = FileBasedCustomerRepository('data/customers.json')
    transaction_repo = FileBasedTransactionRepository('data/transactions.json')
    
    # Create sample customers
    customers = [
        Customer(
            customer_id="CUST001",
            name="Acme Corporation",
            email="billing@acme.com",
            billing_cycle=BillingCycle.MONTHLY,
            created_date=datetime(2023, 1, 15),
            metadata={"industry": "technology", "tier": "enterprise"}
        ),
        Customer(
            customer_id="CUST002",
            name="Global Industries",
            email="finance@global.com",
            billing_cycle=BillingCycle.YEARLY,
            created_date=datetime(2023, 3, 20),
            metadata={"industry": "manufacturing", "tier": "premium"}
        ),
        Customer(
            customer_id="CUST003",
            name="Startup Inc",
            email="admin@startup.com",
            billing_cycle=BillingCycle.MONTHLY,
            created_date=datetime(2023, 6, 10),
            metadata={"industry": "startup", "tier": "basic"}
        )
    ]
    
    # Save customers
    for customer in customers:
        customer_repo.save_customer(customer)
    
    # Create sample transactions for 2024
    transactions = []
    
    # Acme Corporation transactions (high volume customer)
    for month in range(1, 13):
        # Monthly subscription
        transactions.append(Transaction(
            transaction_id=str(uuid.uuid4()),
            customer_id="CUST001",
            amount=Decimal("5000.00"),
            currency="USD",
            transaction_type=TransactionType.PAYMENT,
            transaction_date=datetime(2024, month, 15),
            description=f"Monthly subscription - {month}/2024"
        ))
        
        # Additional services (every other month)
        if month % 2 == 0:
            transactions.append(Transaction(
                transaction_id=str(uuid.uuid4()),
                customer_id="CUST001",
                amount=Decimal("1500.00"),
                currency="USD",
                transaction_type=TransactionType.FEE,
                transaction_date=datetime(2024, month, 20),
                description=f"Premium support fee - {month}/2024"
            ))
    
    # Global Industries transactions (yearly customer)
    transactions.append(Transaction(
        transaction_id=str(uuid.uuid4()),
        customer_id="CUST002",
        amount=Decimal("50000.00"),
        currency="USD",
        transaction_type=TransactionType.PAYMENT,
        transaction_date=datetime(2024, 3, 20),
        description="Annual subscription 2024"
    ))
    
    # Quarterly fees for Global Industries
    for quarter in [3, 6, 9, 12]:
        transactions.append(Transaction(
            transaction_id=str(uuid.uuid4()),
            customer_id="CUST002",
            amount=Decimal("2500.00"),
            currency="USD",
            transaction_type=TransactionType.FEE,
            transaction_date=datetime(2024, quarter, 15),
            description=f"Quarterly maintenance fee - Q{quarter//3}/2024"
        ))
    
    # Startup Inc transactions (smaller customer)
    for month in range(1, 13):
        transactions.append(Transaction(
            transaction_id=str(uuid.uuid4()),
            customer_id="CUST003",
            amount=Decimal("500.00"),
            currency="USD",
            transaction_type=TransactionType.PAYMENT,
            transaction_date=datetime(2024, month, 1),
            description=f"Monthly subscription - {month}/2024"
        ))
        
        # Occasional refunds
        if month in [3, 7, 11]:
            transactions.append(Transaction(
                transaction_id=str(uuid.uuid4()),
                customer_id="CUST003",
                amount=Decimal("-100.00"),
                currency="USD",
                transaction_type=TransactionType.REFUND,
                transaction_date=datetime(2024, month, 10),
                description=f"Service credit - {month}/2024"
            ))
    
    # Save transactions
    for transaction in transactions:
        transaction_repo.save_transaction(transaction)
    
    print("✅ Sample data created successfully!")
    return customer_repo, transaction_repo


def demonstrate_cost_calculations():
    """Demonstrate cost calculation features."""
    print("\n" + "="*80)
    print("💰 COST CALCULATION DEMONSTRATION 💰")
    print("="*80)
    
    # Create repositories
    customer_repo = FileBasedCustomerRepository('data/customers.json')
    transaction_repo = FileBasedTransactionRepository('data/transactions.json')
    
    # Create services
    cost_calculation_service = CostCalculationService(customer_repo, transaction_repo)
    
    # Calculate monthly costs for Acme Corporation
    print("\n📊 Monthly Cost Calculation for Acme Corporation:")
    for month in range(1, 13):
        monthly_cost = cost_calculation_service.calculate_monthly_costs("CUST001", 2024, month)
        print(f"  {month:2d}/2024: ${monthly_cost.total_amount:8,.2f} ({monthly_cost.transaction_count} transactions)")
    
    # Calculate yearly costs
    print("\n📈 Yearly Cost Calculation:")
    for customer_id in ["CUST001", "CUST002", "CUST003"]:
        yearly_cost = cost_calculation_service.calculate_yearly_costs(customer_id, 2024)
        customer = customer_repo.get_customer(customer_id)
        print(f"  {customer.name}: ${yearly_cost.total_amount:10,.2f} ({yearly_cost.transaction_count} transactions)")


def demonstrate_cost_reporting():
    """Demonstrate cost reporting features."""
    print("\n" + "="*80)
    print("📋 COST REPORTING DEMONSTRATION 📋")
    print("="*80)
    
    # Create repositories and services
    customer_repo = FileBasedCustomerRepository('data/customers.json')
    transaction_repo = FileBasedTransactionRepository('data/transactions.json')
    cost_calculation_service = CostCalculationService(customer_repo, transaction_repo)
    cost_reporting_service = CostReportingService(cost_calculation_service)
    presenter = CostReportPresenter()
    
    # Generate customer cost report
    print("\n📊 Customer Cost Report for Acme Corporation:")
    report = cost_reporting_service.generate_customer_cost_report("CUST001", 2024)
    formatted_report = presenter.format_customer_cost_report(report)
    print(formatted_report)
    
    # Generate aggregate report
    print("\n🏢 Aggregate Report for 2024:")
    aggregate_data = cost_reporting_service.generate_aggregate_report(2024)
    formatted_aggregate = presenter.format_aggregate_report(aggregate_data)
    print(formatted_aggregate)


def demonstrate_cost_analysis():
    """Demonstrate cost analysis features."""
    print("\n" + "="*80)
    print("📈 COST ANALYSIS DEMONSTRATION 📈")
    print("="*80)
    
    # Create repositories and services
    customer_repo = FileBasedCustomerRepository('data/customers.json')
    transaction_repo = FileBasedTransactionRepository('data/transactions.json')
    cost_calculation_service = CostCalculationService(customer_repo, transaction_repo)
    cost_analysis_service = CostAnalysisService(cost_calculation_service)
    presenter = CostReportPresenter()
    
    # Analyze cost trends
    print("\n📈 Cost Trends Analysis for Acme Corporation:")
    trends = cost_analysis_service.analyze_cost_trends("CUST001", 2023, 2024)
    formatted_trends = presenter.format_cost_trends(trends)
    print(formatted_trends)
    
    # Identify cost anomalies
    print("\n⚠️  Cost Anomalies Detection:")
    anomalies = cost_analysis_service.identify_cost_anomalies("CUST001", 2024, threshold=1.5)
    formatted_anomalies = presenter.format_cost_anomalies(anomalies)
    print(formatted_anomalies)


def demonstrate_export_features():
    """Demonstrate export features."""
    print("\n" + "="*80)
    print("📤 EXPORT FEATURES DEMONSTRATION 📤")
    print("="*80)
    
    # Create repositories and services
    customer_repo = FileBasedCustomerRepository('data/customers.json')
    transaction_repo = FileBasedTransactionRepository('data/transactions.json')
    cost_calculation_service = CostCalculationService(customer_repo, transaction_repo)
    cost_reporting_service = CostReportingService(cost_calculation_service)
    presenter = CostReportPresenter()
    exporter = CostReportExporter(presenter)
    
    # Generate report and export
    report = cost_reporting_service.generate_customer_cost_report("CUST001", 2024)
    
    # Export to CSV
    csv_filename = "exports/acme_corporation_2024_report.csv"
    os.makedirs("exports", exist_ok=True)
    exporter.export_to_csv(report, csv_filename)
    print(f"✅ Report exported to CSV: {csv_filename}")
    
    # Export to JSON
    json_filename = "exports/acme_corporation_2024_report.json"
    exporter.export_to_json(report, json_filename)
    print(f"✅ Report exported to JSON: {json_filename}")


def main():
    """Main demonstration function."""
    print("🚀 COST EXPLORER SYSTEM DEMONSTRATION 🚀")
    print("="*80)
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    
    # Create sample data
    create_sample_data()
    
    # Demonstrate features
    demonstrate_cost_calculations()
    demonstrate_cost_reporting()
    demonstrate_cost_analysis()
    demonstrate_export_features()
    
    print("\n" + "="*80)
    print("🎉 DEMONSTRATION COMPLETED SUCCESSFULLY! 🎉")
    print("="*80)
    print("\n📁 Generated files:")
    print("  - data/customers.json")
    print("  - data/transactions.json")
    print("  - exports/acme_corporation_2024_report.csv")
    print("  - exports/acme_corporation_2024_report.json")


if __name__ == "__main__":
    main() 