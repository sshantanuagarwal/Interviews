from typing import List, Dict, Any
from datetime import datetime
from decimal import Decimal
from tabulate import tabulate

from models import CustomerCostReport, CostSummary, TransactionType
from services import CostAnalysisService


class CostReportPresenter:
    """Presenter for formatting cost reports for display."""
    
    def __init__(self):
        self.month_names = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
    
    def format_customer_cost_report(self, report: CustomerCostReport) -> str:
        """Format a customer cost report for display."""
        output = []
        
        # Header
        output.append("=" * 80)
        output.append(f"💰 CUSTOMER COST REPORT - {report.customer.name.upper()} 💰")
        output.append("=" * 80)
        output.append(f"Customer ID: {report.customer.customer_id}")
        output.append(f"Email: {report.customer.email}")
        output.append(f"Billing Cycle: {report.customer.billing_cycle.value}")
        output.append(f"Report Generated: {report.generated_date.strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("")
        
        # Summary
        output.append("📊 SUMMARY")
        output.append("-" * 40)
        summary_data = [
            ["Total Yearly Amount", f"{report.currency} {report.total_yearly_amount:,.2f}"],
            ["Average Monthly Amount", f"{report.currency} {report.average_monthly_amount:,.2f}"],
            ["Average Yearly Amount", f"{report.currency} {report.average_yearly_amount:,.2f}"],
            ["Total Monthly Amount", f"{report.currency} {report.total_monthly_amount:,.2f}"]
        ]
        output.append(tabulate(summary_data, headers=["Metric", "Value"], tablefmt="grid"))
        output.append("")
        
        # Monthly Breakdown
        output.append("📅 MONTHLY BREAKDOWN")
        output.append("-" * 40)
        
        monthly_data = []
        for i, monthly_cost in enumerate(report.monthly_costs):
            month_name = self.month_names[i]
            monthly_data.append([
                month_name,
                f"{report.currency} {monthly_cost.total_amount:,.2f}",
                monthly_cost.transaction_count,
                self._format_breakdown(monthly_cost.breakdown, report.currency)
            ])
        
        output.append(tabulate(
            monthly_data,
            headers=["Month", "Total Amount", "Transactions", "Breakdown"],
            tablefmt="grid"
        ))
        output.append("")
        
        # Yearly Breakdown
        output.append("📈 YEARLY BREAKDOWN")
        output.append("-" * 40)
        
        yearly_data = []
        for yearly_cost in report.yearly_costs:
            yearly_data.append([
                f"{yearly_cost.period_start.year}",
                f"{report.currency} {yearly_cost.total_amount:,.2f}",
                yearly_cost.transaction_count,
                self._format_breakdown(yearly_cost.breakdown, report.currency)
            ])
        
        output.append(tabulate(
            yearly_data,
            headers=["Year", "Total Amount", "Transactions", "Breakdown"],
            tablefmt="grid"
        ))
        
        return "\n".join(output)
    
    def format_aggregate_report(self, aggregate_data: Dict[str, Any]) -> str:
        """Format an aggregate report for display."""
        output = []
        
        # Header
        output.append("=" * 80)
        output.append(f"🏢 AGGREGATE COST REPORT - {aggregate_data['year']} 🏢")
        output.append("=" * 80)
        output.append(f"Total Customers: {aggregate_data['total_customers']}")
        output.append(f"Total Revenue: {aggregate_data['total_revenue']:,.2f}")
        output.append("")
        
        # Top Customers
        output.append("🏆 TOP CUSTOMERS")
        output.append("-" * 40)
        
        top_customers_data = []
        for i, report in enumerate(aggregate_data['top_customers'], 1):
            top_customers_data.append([
                i,
                report.customer.name,
                report.customer.customer_id,
                f"{report.currency} {report.total_yearly_amount:,.2f}",
                f"{report.currency} {report.average_monthly_amount:,.2f}"
            ])
        
        output.append(tabulate(
            top_customers_data,
            headers=["Rank", "Customer Name", "Customer ID", "Yearly Total", "Avg Monthly"],
            tablefmt="grid"
        ))
        output.append("")
        
        # Monthly Totals
        output.append("📊 MONTHLY TOTALS")
        output.append("-" * 40)
        
        monthly_totals_data = []
        for i, total in enumerate(aggregate_data['monthly_totals']):
            monthly_totals_data.append([
                self.month_names[i],
                f"{total:,.2f}"
            ])
        
        output.append(tabulate(
            monthly_totals_data,
            headers=["Month", "Total Revenue"],
            tablefmt="grid"
        ))
        
        return "\n".join(output)
    
    def format_cost_trends(self, trends: Dict[str, Any]) -> str:
        """Format cost trends analysis for display."""
        output = []
        
        # Header
        output.append("=" * 80)
        output.append(f"📈 COST TRENDS ANALYSIS - Customer {trends['customer_id']} 📈")
        output.append("=" * 80)
        
        if trends['growth_rate'] is not None:
            output.append(f"Growth Rate: {trends['growth_rate']:.2f}%")
        output.append("")
        
        # Yearly Trends
        output.append("📊 YEARLY TRENDS")
        output.append("-" * 40)
        
        yearly_data = []
        for year, total in zip(trends['years'], trends['yearly_totals']):
            yearly_data.append([year, f"{total:,.2f}"])
        
        output.append(tabulate(
            yearly_data,
            headers=["Year", "Total Amount"],
            tablefmt="grid"
        ))
        output.append("")
        
        # Monthly Averages
        output.append("📅 MONTHLY AVERAGES")
        output.append("-" * 40)
        
        monthly_avg_data = []
        for i, avg in enumerate(trends['monthly_averages']):
            monthly_avg_data.append([
                self.month_names[i],
                f"{avg:,.2f}"
            ])
        
        output.append(tabulate(
            monthly_avg_data,
            headers=["Month", "Average Amount"],
            tablefmt="grid"
        ))
        
        return "\n".join(output)
    
    def format_cost_anomalies(self, anomalies: List[Dict[str, Any]]) -> str:
        """Format cost anomalies for display."""
        if not anomalies:
            return "✅ No cost anomalies detected."
        
        output = []
        output.append("⚠️  COST ANOMALIES DETECTED")
        output.append("=" * 50)
        
        anomalies_data = []
        for anomaly in anomalies:
            anomalies_data.append([
                self.month_names[anomaly['month'] - 1],
                f"{anomaly['amount']:,.2f}",
                f"{anomaly['z_score']:.2f}",
                f"{anomaly['expected_range'][0]:,.2f} - {anomaly['expected_range'][1]:,.2f}"
            ])
        
        output.append(tabulate(
            anomalies_data,
            headers=["Month", "Actual Amount", "Z-Score", "Expected Range"],
            tablefmt="grid"
        ))
        
        return "\n".join(output)
    
    def _format_breakdown(self, breakdown: Dict[TransactionType, Decimal], currency: str) -> str:
        """Format transaction breakdown for display."""
        if not breakdown:
            return "No transactions"
        
        parts = []
        for transaction_type, amount in breakdown.items():
            parts.append(f"{transaction_type.value}: {currency} {amount:,.2f}")
        
        return " | ".join(parts)


class CostReportExporter:
    """Exporter for generating cost reports in different formats."""
    
    def __init__(self, presenter: CostReportPresenter):
        self.presenter = presenter
    
    def export_to_csv(self, report: CustomerCostReport, filename: str) -> None:
        """Export cost report to CSV format."""
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['Customer Cost Report'])
            writer.writerow(['Customer ID', report.customer.customer_id])
            writer.writerow(['Customer Name', report.customer.name])
            writer.writerow(['Email', report.customer.email])
            writer.writerow(['Billing Cycle', report.customer.billing_cycle.value])
            writer.writerow(['Generated Date', report.generated_date.strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            
            # Write summary
            writer.writerow(['Summary'])
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Total Yearly Amount', f"{report.currency} {report.total_yearly_amount:,.2f}"])
            writer.writerow(['Average Monthly Amount', f"{report.currency} {report.average_monthly_amount:,.2f}"])
            writer.writerow(['Average Yearly Amount', f"{report.currency} {report.average_yearly_amount:,.2f}"])
            writer.writerow([])
            
            # Write monthly breakdown
            writer.writerow(['Monthly Breakdown'])
            writer.writerow(['Month', 'Total Amount', 'Transactions', 'Breakdown'])
            
            month_names = [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]
            
            for i, monthly_cost in enumerate(report.monthly_costs):
                breakdown_str = self.presenter._format_breakdown(monthly_cost.breakdown, report.currency)
                writer.writerow([
                    month_names[i],
                    f"{report.currency} {monthly_cost.total_amount:,.2f}",
                    monthly_cost.transaction_count,
                    breakdown_str
                ])
    
    def export_to_json(self, report: CustomerCostReport, filename: str) -> None:
        """Export cost report to JSON format."""
        import json
        
        report_data = {
            'customer': {
                'customer_id': report.customer.customer_id,
                'name': report.customer.name,
                'email': report.customer.email,
                'billing_cycle': report.customer.billing_cycle.value,
                'created_date': report.customer.created_date.isoformat(),
                'is_active': report.customer.is_active
            },
            'summary': {
                'total_yearly_amount': float(report.total_yearly_amount),
                'average_monthly_amount': float(report.average_monthly_amount),
                'average_yearly_amount': float(report.average_yearly_amount),
                'total_monthly_amount': float(report.total_monthly_amount),
                'currency': report.currency,
                'generated_date': report.generated_date.isoformat()
            },
            'monthly_costs': [
                {
                    'period_start': cost.period_start.isoformat(),
                    'period_end': cost.period_end.isoformat(),
                    'total_amount': float(cost.total_amount),
                    'transaction_count': cost.transaction_count,
                    'breakdown': {k.value: float(v) for k, v in cost.breakdown.items()}
                }
                for cost in report.monthly_costs
            ],
            'yearly_costs': [
                {
                    'period_start': cost.period_start.isoformat(),
                    'period_end': cost.period_end.isoformat(),
                    'total_amount': float(cost.total_amount),
                    'transaction_count': cost.transaction_count,
                    'breakdown': {k.value: float(v) for k, v in cost.breakdown.items()}
                }
                for cost in report.yearly_costs
            ]
        }
        
        with open(filename, 'w') as jsonfile:
            json.dump(report_data, jsonfile, indent=2) 