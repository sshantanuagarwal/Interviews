#!/usr/bin/env python3
"""
Command Line Interface for the Cost Explorer system.

Usage:
    python -m cost_explorer.cli <command> [options]
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from cost_explorer import (
    FileBasedCustomerRepository, FileBasedTransactionRepository,
    CostCalculationService, CostReportingService, CostAnalysisService,
    CostReportPresenter, CostReportExporter
)


def setup_repositories(data_dir: str = "data"):
    """Setup repositories with data directory."""
    Path(data_dir).mkdir(exist_ok=True)
    
    customer_repo = FileBasedCustomerRepository(f"{data_dir}/customers.json")
    transaction_repo = FileBasedTransactionRepository(f"{data_dir}/transactions.json")
    
    return customer_repo, transaction_repo


def cmd_monthly_cost(args):
    """Calculate monthly costs for a customer."""
    customer_repo, transaction_repo = setup_repositories(args.data_dir)
    cost_service = CostCalculationService(customer_repo, transaction_repo)
    
    monthly_cost = cost_service.calculate_monthly_costs(
        args.customer_id, args.year, args.month
    )
    
    print(f"\n📊 Monthly Cost Report for Customer {args.customer_id}")
    print(f"Period: {args.month}/{args.year}")
    print(f"Total Amount: ${monthly_cost.total_amount:,.2f}")
    print(f"Transactions: {monthly_cost.transaction_count}")
    print(f"Currency: {monthly_cost.currency}")
    
    if monthly_cost.breakdown:
        print("\nBreakdown:")
        for transaction_type, amount in monthly_cost.breakdown.items():
            print(f"  {transaction_type.value}: ${amount:,.2f}")


def cmd_yearly_cost(args):
    """Calculate yearly costs for a customer."""
    customer_repo, transaction_repo = setup_repositories(args.data_dir)
    cost_service = CostCalculationService(customer_repo, transaction_repo)
    
    yearly_cost = cost_service.calculate_yearly_costs(args.customer_id, args.year)
    
    print(f"\n📈 Yearly Cost Report for Customer {args.customer_id}")
    print(f"Year: {args.year}")
    print(f"Total Amount: ${yearly_cost.total_amount:,.2f}")
    print(f"Transactions: {yearly_cost.transaction_count}")
    print(f"Currency: {yearly_cost.currency}")
    
    if yearly_cost.breakdown:
        print("\nBreakdown:")
        for transaction_type, amount in yearly_cost.breakdown.items():
            print(f"  {transaction_type.value}: ${amount:,.2f}")


def cmd_customer_report(args):
    """Generate comprehensive customer cost report."""
    customer_repo, transaction_repo = setup_repositories(args.data_dir)
    cost_service = CostCalculationService(customer_repo, transaction_repo)
    reporting_service = CostReportingService(cost_service)
    presenter = CostReportPresenter()
    
    try:
        report = reporting_service.generate_customer_cost_report(args.customer_id, args.year)
        formatted_report = presenter.format_customer_cost_report(report)
        print(formatted_report)
        
        if args.export:
            exporter = CostReportExporter(presenter)
            Path("exports").mkdir(exist_ok=True)
            
            csv_filename = f"exports/{args.customer_id}_{args.year}_report.csv"
            json_filename = f"exports/{args.customer_id}_{args.year}_report.json"
            
            exporter.export_to_csv(report, csv_filename)
            exporter.export_to_json(report, json_filename)
            
            print(f"\n✅ Reports exported to:")
            print(f"  - {csv_filename}")
            print(f"  - {json_filename}")
            
    except ValueError as e:
        print(f"❌ Error: {e}")


def cmd_aggregate_report(args):
    """Generate aggregate report for all customers."""
    customer_repo, transaction_repo = setup_repositories(args.data_dir)
    cost_service = CostCalculationService(customer_repo, transaction_repo)
    reporting_service = CostReportingService(cost_service)
    presenter = CostReportPresenter()
    
    aggregate_data = reporting_service.generate_aggregate_report(args.year)
    formatted_report = presenter.format_aggregate_report(aggregate_data)
    print(formatted_report)


def cmd_cost_trends(args):
    """Analyze cost trends for a customer."""
    customer_repo, transaction_repo = setup_repositories(args.data_dir)
    cost_service = CostCalculationService(customer_repo, transaction_repo)
    analysis_service = CostAnalysisService(cost_service)
    presenter = CostReportPresenter()
    
    trends = analysis_service.analyze_cost_trends(
        args.customer_id, args.start_year, args.end_year
    )
    formatted_trends = presenter.format_cost_trends(trends)
    print(formatted_trends)


def cmd_anomalies(args):
    """Detect cost anomalies for a customer."""
    customer_repo, transaction_repo = setup_repositories(args.data_dir)
    cost_service = CostCalculationService(customer_repo, transaction_repo)
    analysis_service = CostAnalysisService(cost_service)
    presenter = CostReportPresenter()
    
    anomalies = analysis_service.identify_cost_anomalies(
        args.customer_id, args.year, args.threshold
    )
    formatted_anomalies = presenter.format_cost_anomalies(anomalies)
    print(formatted_anomalies)


def cmd_list_customers(args):
    """List all customers."""
    customer_repo, _ = setup_repositories(args.data_dir)
    customers = customer_repo.get_all_customers()
    
    if not customers:
        print("No customers found.")
        return
    
    print(f"\n📋 Customers ({len(customers)} total):")
    print("-" * 80)
    
    for customer in customers:
        status = "✅ Active" if customer.is_active else "❌ Inactive"
        print(f"ID: {customer.customer_id}")
        print(f"Name: {customer.name}")
        print(f"Email: {customer.email}")
        print(f"Billing Cycle: {customer.billing_cycle.value}")
        print(f"Status: {status}")
        print(f"Created: {customer.created_date.strftime('%Y-%m-%d')}")
        print("-" * 80)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Cost Explorer - Calculate and analyze customer costs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate monthly costs
  python -m cost_explorer.cli monthly CUST001 --year 2024 --month 6
  
  # Generate customer report
  python -m cost_explorer.cli report CUST001 --year 2024 --export
  
  # Analyze trends
  python -m cost_explorer.cli trends CUST001 --start-year 2023 --end-year 2024
  
  # Detect anomalies
  python -m cost_explorer.cli anomalies CUST001 --year 2024 --threshold 2.0
        """
    )
    
    parser.add_argument(
        '--data-dir', 
        default='data',
        help='Data directory (default: data)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Monthly cost command
    monthly_parser = subparsers.add_parser('monthly', help='Calculate monthly costs')
    monthly_parser.add_argument('customer_id', help='Customer ID')
    monthly_parser.add_argument('--year', type=int, required=True, help='Year')
    monthly_parser.add_argument('--month', type=int, required=True, help='Month (1-12)')
    monthly_parser.set_defaults(func=cmd_monthly_cost)
    
    # Yearly cost command
    yearly_parser = subparsers.add_parser('yearly', help='Calculate yearly costs')
    yearly_parser.add_argument('customer_id', help='Customer ID')
    yearly_parser.add_argument('--year', type=int, required=True, help='Year')
    yearly_parser.set_defaults(func=cmd_yearly_cost)
    
    # Customer report command
    report_parser = subparsers.add_parser('report', help='Generate customer cost report')
    report_parser.add_argument('customer_id', help='Customer ID')
    report_parser.add_argument('--year', type=int, required=True, help='Year')
    report_parser.add_argument('--export', action='store_true', help='Export to CSV/JSON')
    report_parser.set_defaults(func=cmd_customer_report)
    
    # Aggregate report command
    aggregate_parser = subparsers.add_parser('aggregate', help='Generate aggregate report')
    aggregate_parser.add_argument('--year', type=int, required=True, help='Year')
    aggregate_parser.set_defaults(func=cmd_aggregate_report)
    
    # Trends command
    trends_parser = subparsers.add_parser('trends', help='Analyze cost trends')
    trends_parser.add_argument('customer_id', help='Customer ID')
    trends_parser.add_argument('--start-year', type=int, required=True, help='Start year')
    trends_parser.add_argument('--end-year', type=int, required=True, help='End year')
    trends_parser.set_defaults(func=cmd_cost_trends)
    
    # Anomalies command
    anomalies_parser = subparsers.add_parser('anomalies', help='Detect cost anomalies')
    anomalies_parser.add_argument('customer_id', help='Customer ID')
    anomalies_parser.add_argument('--year', type=int, required=True, help='Year')
    anomalies_parser.add_argument('--threshold', type=float, default=2.0, help='Z-score threshold')
    anomalies_parser.set_defaults(func=cmd_anomalies)
    
    # List customers command
    list_parser = subparsers.add_parser('list', help='List all customers')
    list_parser.set_defaults(func=cmd_list_customers)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 