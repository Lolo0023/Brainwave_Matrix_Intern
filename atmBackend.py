import sqlite3
import requests


class ATM_Machine:
    def __init__(self):
        self.connection = sqlite3.connect("ATM_Database.db") 
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            user_account_number TEXT PRIMARY KEY,
            user_PIN TEXT NOT NULL,
            user_balance REAL DEFAULT 0
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_account_number TEXT,
            type TEXT,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.connection.commit()
    
    def create_account(self, user_account_number, user_PIN, user_initial_balance=0):
        self.cursor.execute("SELECT * FROM accounts WHERE user_account_number = ?", (user_account_number,))
        if self.cursor.fetchone():
            raise ValueError("This account already exists")
        self.cursor.execute(
            "INSERT INTO accounts (user_account_number, user_PIN, user_balance) VALUES (?, ?, ?)",
            (user_account_number, user_PIN, user_initial_balance))
        self.connection.commit()
    
    def authentication(self, user_account_number, user_PIN):
        self.cursor.execute("SELECT * FROM accounts WHERE user_account_number = ? AND user_PIN = ?", 
                            (user_account_number, user_PIN))
        return self.cursor.fetchone() is not None
    
    def get_balance(self, user_account_number):
        self.cursor.execute("SELECT user_balance FROM accounts WHERE user_account_number = ?", (user_account_number,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def deposit(self, user_account_number, deposite_amount):    
        self.cursor.execute("UPDATE accounts SET user_balance = user_balance + ? WHERE user_account_number = ?", 
                            (deposite_amount, user_account_number))
        self.cursor.execute("INSERT INTO transactions (user_account_number, type, amount) VALUES (?, ?, ?)",
                        (user_account_number, 'Deposit', deposite_amount))
        self.connection.commit()

    def withdraw(self, user_account_number, withdrawn_amount):
        user_current_balance = self.get_balance(user_account_number)
        if user_current_balance is None:
            raise ValueError("Account not found.")
        
        if withdrawn_amount > user_current_balance:
            raise ValueError("Insufficient funds.")
        
        self.cursor.execute("UPDATE accounts SET user_balance = user_balance - ? WHERE user_account_number = ?", 
                            (withdrawn_amount, user_account_number))
        self.cursor.execute("INSERT INTO transactions (user_account_number, type, amount) VALUES (?, ?, ?)",
                        (user_account_number, 'Withdraw', withdrawn_amount))   
        self.connection.commit()
    
    def get_transaction_history(self, user_account_number):
        self.cursor.execute("SELECT type, amount, timestamp FROM transactions WHERE user_account_number = ? ORDER BY timestamp DESC",
                            (user_account_number,))
        return self.cursor.fetchall()
    
    def get_exchange_rate(self, target_currency):
        try:
            url = "https://open.er-api.com/v6/latest/USD"
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()
            rates = data.get("rates", {})
            return rates.get(target_currency.upper(), None)
        except requests.exceptions.RequestException:
            return None

    def convert_balance(self, user_account_number, target_currency):
        balance = self.get_balance(user_account_number)
        if balance is None:
            raise ValueError("Account not found")

        rate = self.get_exchange_rate(target_currency)
        if rate is None:
            raise ValueError("Failed to fetch exchange rate")

        return round(balance * rate, 2)

    

