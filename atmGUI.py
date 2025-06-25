import tkinter as tk
from tkinter import font
from tkinter import messagebox, simpledialog
from atmBackend import ATM_Machine

class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM System")
        self.ATM = ATM_Machine()
        self.account = None
        self.create_Welcome_page()


    def create_Welcome_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("ATM System - Welcome")
        self.root.geometry("400x350")  # Set window size
        self.root.configure(bg="#f0f4f7")  # Light background

        frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=250)

        title_font = font.Font(family="Helvetica", size=14, weight="bold")
        label_font = font.Font(family="Helvetica", size=11)
        entry_font = font.Font(size=11)

        tk.Label(frame, text="Welcome to ATM", font=title_font, bg="white", fg="#2c3e50").pack(pady=(10, 15))

        tk.Label(frame, text="Account Number", font=label_font, bg="white").pack()
        self.account_entry = tk.Entry(frame, font=entry_font, width=25)
        self.account_entry.pack(pady=5)

        tk.Label(frame, text="PIN", font=label_font, bg="white").pack()
        self.pin_entry = tk.Entry(frame, show="*", font=entry_font, width=25)
        self.pin_entry.pack(pady=5)

        tk.Button(frame, text="Login", font=label_font, bg="#3498db", fg="white", width=15, command=self.login).pack(pady=(10, 5))
        tk.Button(frame, text="Create Account", font=label_font, bg="#2ecc71", fg="white", width=15, command=self.create_account).pack(pady=5)

    
    def create_account(self):
        acc = self.account_entry.get()
        pin = self.pin_entry.get()
    
        if not acc or not pin:
            messagebox.showerror("Error", "Please enter both account number and PIN.")
            return
        if not acc.isdigit() or not len(acc) == 10:
            messagebox.showerror("Error", "Account Number must be 10 digits!")
            return
        if not pin.isdigit() or not len(pin) == 6:
            messagebox.showerror("Error", "PIN must be 6 digits!")
            return
        
    
        try:
            self.ATM.create_account(acc, pin)
            messagebox.showinfo("Success", "Account created. You can now log in.")
        except:
            messagebox.showerror("Error", "Account already exists.")


    def login(self):
        acc = self.account_entry.get()
        pin = self.pin_entry.get()
        if not acc or not pin:
            messagebox.showerror("Error", "Please enter both account number and PIN.")
            return
        if not acc.isdigit() or not len(acc) == 10:
            messagebox.showerror("Error", "Account Number must be 10 digits!")
            return
        if not pin.isdigit() or not len(pin) == 6:
            messagebox.showerror("Error", "PIN must be 6 digits!")
            return
        
        if self.ATM.authentication(acc, pin):
            self.account = acc
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Invalid account")

    def create_main_menu(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("ATM System - Main Menu")
        self.root.geometry("400x400")
        self.root.configure(bg="#f0f4f7")

        frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=350)

        title_font = font.Font(family="Helvetica", size=14, weight="bold")
        button_font = font.Font(family="Helvetica", size=11)

        tk.Label(frame, text="Welcome to the ATM!", font=title_font, bg="white", fg="#2c3e50").pack(pady=(15, 20))

        btn_style = {
            "font": button_font,
            "width": 20,
            "bg": "#3498db",
            "fg": "white",
            "activebackground": "#2980b9",
            "bd": 0,
            "relief": "raised",
            "cursor": "hand2",
        }

        tk.Button(frame, text="Check Balance", command=self.check_balance, **btn_style).pack(pady=5)
        tk.Button(frame, text="Deposit", command=self.deposit, **btn_style).pack(pady=5)
        tk.Button(frame, text="Withdraw", command=self.withdraw, **btn_style).pack(pady=5)
        tk.Button(frame, text="Transaction History", command=self.show_transaction_history, **btn_style).pack(pady=5)
        tk.Button(frame, text="convert currency", command=self.convert_currency, **btn_style).pack(pady=5)
        
        logout_style = btn_style.copy()
        logout_style.update({
            "bg": "#e74c3c",
            "activebackground": "#c0392b"
        })
        tk.Button(frame, text="Logout", command=self.logout, **logout_style).pack(pady=10)


    def deposit(self):
        input_money = simpledialog.askstring("Deposit", "Enter amount to deposit:")
        if not input_money:
            return
        try:
            amount = float(input_money)
            if amount<=0:
                messagebox.showerror("Error","Deposite amount must be greater than 0")
                return
            self.ATM.deposit(self.account, amount)
            messagebox.showinfo("Success", f"deposite ${amount:.2f} successfully.")
        except:
            messagebox.showerror("Error", "Please enter a valid number.")



    def withdraw(self):
        input_money = simpledialog.askstring("Withdraw", "Enter amount to withdraw:")
        if not input_money:
            return
        try:
            amount=float(input_money)
            if input_money<=0:
                messagebox.showerror("Error","Withdrawal amount must be grater than 0")
                return
            self.ATM.withdraw(self.account, amount)
            messagebox.showinfo("Success", f"deposite ${amount:.2f} successfully.")
        except:
            messagebox.showerror("Error", "Transaction declined: Not enough balance.")
            
    def check_balance(self):
        balance = self.ATM.get_balance(self.account)
        messagebox.showinfo("Balance", f"Your balance is ${balance:.2f}")

    def show_transaction_history(self):
        history = self.ATM.get_transaction_history(self.account)
        history_str = "\n".join([f"{t[2]} - {t[0]}: ${t[1]:.2f}" for t in history])
        if not history_str:
            history_str = "No transactions found."
        messagebox.showinfo("Transaction History", history_str)

    def convert_currency(self):
        currency = simpledialog.askstring("Currency Conversion", "Enter target currency code (e.g., EUR, EGP):")

        if not currency:
            return  

        try:
            converted = self.ATM.convert_balance(self.account, currency)
            messagebox.showinfo("Conversion Result", f"Your balance in {currency.upper()} is {converted:.2f}")
        except ValueError as e:
            messagebox.showerror("Conversion Failed", str(e))
        
    def logout(self):
        self.account = None
        self.create_Welcome_page()
    
    

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
