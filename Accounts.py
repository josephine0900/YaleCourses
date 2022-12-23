from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import TypeDecorator

from Transactions import Transaction, Base
import logging
from decimal import Decimal
from datetime import timedelta, date, datetime

class OverdrawError(Exception):
    pass

class TransactionLimitError(Exception):
    pass

class TransactionSequenceError(Exception):
    def __init__(self, date):
        super().__init__()
        self.latest_date = date

class MyAmount(TypeDecorator):
    """Converts strings to handle decimal values."""

    impl = String

    def __init__(self, length=None, **kwargs):
        super().__init__(length, **kwargs)
        self.format = format
        
    # literal converts 
    def process_literal_param(self, value, dialect):
        # convert python time to sql string
        return str(value) if value is not None else None

    process_bind_param = process_literal_param

    def process_result_value(self, value, dialect):
        # convert sql string to python decimal
        return Decimal(value) if value is not None else None

class Account(Base):
    """This is an abstract class for accounts.  Provides default functionality for adding transactions, getting balances, and assessing interest and fees.  
    Accounts should be instantiated as SavingsAccounts or CheckingAccounts
    """

    __tablename__ = "account"

    _id = Column(Integer, primary_key=True)
    _bank_id = Column(Integer, ForeignKey("bank._id"))
    _account_number = Column(Integer)
    _interest_rate = Column(MyAmount(length=30))
    _type = Column(String(50))
    _transactions = relationship("Transaction", backref=backref("account"))

    __mapper_args__ = {
        'polymorphic_identity':'account',
        'polymorphic_on':_type
    }

    def __init__(self, acct_num):
        self._account_number = acct_num
        logging.debug(f"Created account: {self._account_number}")

    def add_transaction(self, amt, session, date=None, exempt=False):
        """Creates a new transaction and checks to see if it is allowed, adding it to the account if it is.

        Args:
            amt (Decimal): amount for new transaction
            date (Date, optional): Date for the new transaction. Defaults to None.
            exempt (bool, optional): Determines whether the transaction is exempt from account limits. Defaults to False.
        """

        t = Transaction(amt,
                        self._account_number,
                        date=date, 
                        exempt=exempt)

        if not t.is_exempt():
            self._check_balance(t)
            self._check_limits(t)
            self._check_date(t)
        self._transactions.append(t)
        session.add(t)

    def _check_balance(self, t):
        """Checks whether an incoming transaction would overdraw the account

        Args:
            t (Transaction): pending transaction

        Returns:
            bool: false if account is overdrawn
        """
        if not t.check_balance(self.get_balance()):
            raise OverdrawError()

    def _check_limits(self, t):
        pass

    def _check_date(self, t):
        """Checks the date of the given transaction to the most recent transaction."""
        if len(self._transactions) > 0:
            latest_transaction = max(self._transactions)
            if t < latest_transaction:
                raise TransactionSequenceError(latest_transaction.date)

    def get_balance(self):
        """Gets the balance for an account by summing its transactions

        Returns:
            float: current balance
        """
        # could have a balance variable updated when transactions are added (or removed) which is faster
        # but this is more foolproof since it's always in sync with transactions
        return sum(x for x in self._transactions)

    def _assess_interest(self, latest_transaction, session):
        """Calculates interest for an account balance and adds it as a new transaction exempt from limits.
        """
        self.add_transaction(self.get_balance() * self._interest_rate, session, 
                        date=latest_transaction.last_day_of_month(), 
                        exempt=True)

    def _assess_fees(self, lt, session):
        pass

    def assess_interest_and_fees(self, session):
        """Used to apply interest and/or fees for this account

        Raises:
            TransactionSequenceError: Indicates that the new transactions were
            not newer than the most recent interest or fees transactions
        """
        latest_transaction = max(self._transactions)
        for t in self._transactions:
            if t.is_exempt() and t.in_same_month(latest_transaction):
                # found an interest or fee transaction that is already in the
                # same month as the most recent transaction
                raise TransactionSequenceError(t.date)
        self._assess_interest(latest_transaction, session)
        self._assess_fees(latest_transaction, session)


    
    def __str__(self):
        """Formats the account number and balance of the account.
        For example, '#000000001,<tab>balance: $50.00'
        """    
        return f"#{self._account_number:09},\tbalance: ${self.get_balance():,.2f}"

    def get_transactions(self):
        """Get list of transactions for selected account."""
        return self._transactions


class SavingsAccount(Account):
    """Concrete Account class with daily and monthly account limits and high interest rate.
    """    
    _daily_limit = Column(MyAmount(length=30))
    _monthly_limit = Column(MyAmount(length=30))

    __mapper_args__ = {
        'polymorphic_identity':'savingsaccount',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._interest_rate = Decimal("0.025")
        self._daily_limit = 2
        self._monthly_limit = 5

    def _check_limits(self, t1):
        """determines if the incoming trasaction is within the accounts transaction limits

        Args:
            t1 (Transaction): pending transaction to be checked

        Returns:
            bool: true if within limits and false if beyond limits
        """    
        num_today = len(
            [t2 for t2 in self._transactions if not t2.is_exempt() and t2.in_same_day(t1)])
        num_this_month = len(
            [t2 for t2 in self._transactions if not t2.is_exempt() and t2.in_same_month(t1)])
        if  ( num_today >= self._daily_limit or num_this_month >= self._monthly_limit):
            raise TransactionLimitError()

    def __str__(self):
        """Formats the type, account number, and balance of the account.
        For example, 'Savings#000000001,<tab>balance: $50.00'
        """ 
        return "Savings" + super().__str__()


class CheckingAccount(Account):
    """Concrete Account class with lower interest rate and low balance fees.
    """  

    _balance_threshold = Column(MyAmount(length=30))
    _low_balance_fee = Column(MyAmount(length=30))

    __mapper_args__ = {
        'polymorphic_identity':'checkingaccount',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._interest_rate = Decimal("0.0015")
        self._balance_threshold = 100
        self._low_balance_fee = -10



    def _assess_fees(self, latest_transaction, session):
        """Adds a low balance fee if balance is below a particular threshold. Fee amount and balance threshold are defined on the CheckingAccount.
        """
        if self.get_balance() < self._balance_threshold:
            self.add_transaction(self._low_balance_fee, session,
                                 date=latest_transaction.last_day_of_month(), 
                                 exempt=True)

    def __str__(self):
        """Formats the type, account number, and balance of the account.
        For example, 'Checking#000000001,<tab>balance: $50.00'
        """ 
        return "Checking" + super().__str__()
