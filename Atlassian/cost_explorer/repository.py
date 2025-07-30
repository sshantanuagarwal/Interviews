from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import json
import csv
from pathlib import Path

from models import Customer, Transaction, CostSummary, CustomerCostReport, TransactionType, BillingCycle


class CustomerRepository(ABC):
    """Abstract base class for customer data access."""
    
    @abstractmethod
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID."""
        pass
    
    @abstractmethod
    def get_all_customers(self) -> List[Customer]:
        """Get all customers."""
        pass
    
    @abstractmethod
    def save_customer(self, customer: Customer) -> None:
        """Save customer data."""
        pass
    
    @abstractmethod
    def update_customer(self, customer: Customer) -> None:
        """Update customer data."""
        pass


class TransactionRepository(ABC):
    """Abstract base class for transaction data access."""
    
    @abstractmethod
    def get_transactions_by_customer(self, customer_id: str, 
                                   start_date: Optional[date] = None,
                                   end_date: Optional[date] = None) -> List[Transaction]:
        """Get transactions for a specific customer within date range."""
        pass
    
    @abstractmethod
    def get_transactions_by_period(self, start_date: date, end_date: date) -> List[Transaction]:
        """Get all transactions within a date period."""
        pass
    
    @abstractmethod
    def save_transaction(self, transaction: Transaction) -> None:
        """Save transaction data."""
        pass


class FileBasedCustomerRepository(CustomerRepository):
    """File-based implementation of customer repository."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.customers: Dict[str, Customer] = {}
        self._load_customers()
    
    def _load_customers(self):
        """Load customers from file."""
        if not self.file_path.exists():
            return
        
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            for customer_data in data:
                customer = Customer(
                    customer_id=customer_data['customer_id'],
                    name=customer_data['name'],
                    email=customer_data['email'],
                    billing_cycle=BillingCycle(customer_data['billing_cycle']),
                    created_date=datetime.fromisoformat(customer_data['created_date']),
                    is_active=customer_data.get('is_active', True),
                    metadata=customer_data.get('metadata', {})
                )
                self.customers[customer.customer_id] = customer
    
    def _save_customers(self):
        """Save customers to file."""
        data = []
        for customer in self.customers.values():
            customer_data = {
                'customer_id': customer.customer_id,
                'name': customer.name,
                'email': customer.email,
                'billing_cycle': customer.billing_cycle.value,
                'created_date': customer.created_date.isoformat(),
                'is_active': customer.is_active,
                'metadata': customer.metadata
            }
            data.append(customer_data)
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        return self.customers.get(customer_id)
    
    def get_all_customers(self) -> List[Customer]:
        return list(self.customers.values())
    
    def save_customer(self, customer: Customer) -> None:
        self.customers[customer.customer_id] = customer
        self._save_customers()
    
    def update_customer(self, customer: Customer) -> None:
        self.customers[customer.customer_id] = customer
        self._save_customers()


class FileBasedTransactionRepository(TransactionRepository):
    """File-based implementation of transaction repository."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.transactions: List[Transaction] = []
        self._load_transactions()
    
    def _load_transactions(self):
        """Load transactions from file."""
        if not self.file_path.exists():
            return
        
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            for transaction_data in data:
                transaction = Transaction(
                    transaction_id=transaction_data['transaction_id'],
                    customer_id=transaction_data['customer_id'],
                    amount=Decimal(transaction_data['amount']),
                    currency=transaction_data['currency'],
                    transaction_type=TransactionType(transaction_data['transaction_type']),
                    transaction_date=datetime.fromisoformat(transaction_data['transaction_date']),
                    description=transaction_data['description'],
                    reference_id=transaction_data.get('reference_id'),
                    metadata=transaction_data.get('metadata', {})
                )
                self.transactions.append(transaction)
    
    def _save_transactions(self):
        """Save transactions to file."""
        data = []
        for transaction in self.transactions:
            transaction_data = {
                'transaction_id': transaction.transaction_id,
                'customer_id': transaction.customer_id,
                'amount': str(transaction.amount),
                'currency': transaction.currency,
                'transaction_type': transaction.transaction_type.value,
                'transaction_date': transaction.transaction_date.isoformat(),
                'description': transaction.description,
                'reference_id': transaction.reference_id,
                'metadata': transaction.metadata
            }
            data.append(transaction_data)
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_transactions_by_customer(self, customer_id: str, 
                                   start_date: Optional[date] = None,
                                   end_date: Optional[date] = None) -> List[Transaction]:
        filtered_transactions = [
            t for t in self.transactions 
            if t.customer_id == customer_id
        ]
        
        if start_date:
            filtered_transactions = [
                t for t in filtered_transactions 
                if t.transaction_date.date() >= start_date
            ]
        
        if end_date:
            filtered_transactions = [
                t for t in filtered_transactions 
                if t.transaction_date.date() <= end_date
            ]
        
        return filtered_transactions
    
    def get_transactions_by_period(self, start_date: date, end_date: date) -> List[Transaction]:
        return [
            t for t in self.transactions 
            if start_date <= t.transaction_date.date() <= end_date
        ]
    
    def save_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)
        self._save_transactions() 