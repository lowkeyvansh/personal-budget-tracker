import tkinter as tk
from tkinter import messagebox
import json
import os

def setup_window():
    root = tk.Tk()
    root.title("Personal Budget Tracker")
    root.geometry("500x600")
    return root

def create_input_fields(root):
    tk.Label(root, text="Amount:").pack(pady=5)
    amount_entry = tk.Entry(root, width=20)
    amount_entry.pack(pady=5)

    tk.Label(root, text="Description:").pack(pady=5)
    description_entry = tk.Entry(root, width=40)
    description_entry.pack(pady=5)

    tk.Label(root, text="Category:").pack(pady=5)
    category_entry = tk.Entry(root, width=40)
    category_entry.pack(pady=5)

    return amount_entry, description_entry, category_entry

def create_buttons(root, add_income, add_expense):
    income_button = tk.Button(root, text="Add Income", command=add_income)
    income_button.pack(pady=10)

    expense_button = tk.Button(root, text="Add Expense", command=add_expense)
    expense_button.pack(pady=10)

    return income_button, expense_button

def load_data():
    if os.path.exists("budget_data.json"):
        with open("budget_data.json", "r") as file:
            return json.load(file)
    return {"income": [], "expenses": []}

def save_data(data):
    with open("budget_data.json", "w") as file:
        json.dump(data, file, indent=4)

def add_transaction(amount_entry, description_entry, category_entry, transaction_type):
    amount = amount_entry.get().strip()
    description = description_entry.get().strip()
    category = category_entry.get().strip()

    if amount and description and category:
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        data = load_data()
        transaction = {
            "amount": amount,
            "description": description,
            "category": category
        }

        if transaction_type == "income":
            data["income"].append(transaction)
        else:
            data["expenses"].append(transaction)

        save_data(data)
        amount_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"{transaction_type.capitalize()} added successfully!")
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

def display_summary(root):
    summary_frame = tk.Frame(root)
    summary_frame.pack(pady=20)

    data = load_data()
    total_income = sum(item["amount"] for item in data["income"])
    total_expenses = sum(item["amount"] for item in data["expenses"])
    balance = total_income - total_expenses

    tk.Label(summary_frame, text=f"Total Income: ${total_income:.2f}").pack()
    tk.Label(summary_frame, text=f"Total Expenses: ${total_expenses:.2f}").pack()
    tk.Label(summary_frame, text=f"Balance: ${balance:.2f}").pack()

    return summary_frame

def main():
    root = setup_window()

    amount_entry, description_entry, category_entry = create_input_fields(root)

    add_income = lambda: add_transaction(amount_entry, description_entry, category_entry, "income")
    add_expense = lambda: add_transaction(amount_entry, description_entry, category_entry, "expense")
    
    create_buttons(root, add_income, add_expense)

    summary_frame = display_summary(root)
    
    def refresh_summary():
        nonlocal summary_frame
        summary_frame.destroy()
        summary_frame = display_summary(root)
    
    add_income = lambda: [add_transaction(amount_entry, description_entry, category_entry, "income"), refresh_summary()]
    add_expense = lambda: [add_transaction(amount_entry, description_entry, category_entry, "expense"), refresh_summary()]

    root.mainloop()

if __name__ == "__main__":
    main()
