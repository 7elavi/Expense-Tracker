import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DB_NAME = "expenses.json"

def load_data():
    if os.path.exists(DB_NAME):
        try:
            with open(DB_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(DB_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_entry():
    raw_amount = ent_amount.get().strip()
    cat = cb_cat.get().strip()
    raw_date = ent_date.get().strip()

    if not raw_amount or not cat or not raw_date:
        messagebox.showwarning("Ввод", "Заполните все поля")
        return

    try:
        amount = float(raw_amount)
        if amount <= 0: raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
        return

    try:
        datetime.strptime(raw_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Формат даты: ГГГГ-ММ-ДД")
        return

    expenses.append({"amount": amount, "category": cat, "date": raw_date})
    save_data(expenses)
    refresh_ui(expenses)
    ent_amount.delete(0, tk.END)

def refresh_ui(data_list):
    for i in tree.get_children():
        tree.delete(i)
    total = 0
    for item in data_list:
        tree.insert("", tk.END, values=(item["date"], item["category"], f"{item['amount']:.2f}"))
        total += item["amount"]
    lbl_total.config(text=f"Итого за период: {total:.2f}")

def apply_filters():
    f_cat = cb_f_cat.get()
    f_start = ent_f_start.get().strip()
    f_end = ent_f_end.get().strip()
    
    res = expenses
    if f_cat and f_cat != "Все":
        res = [x for x in res if x["category"] == f_cat]
    
    try:
        if f_start:
            sd = datetime.strptime(f_start, "%Y-%m-%d")
            res = [x for x in res if datetime.strptime(x["date"], "%Y-%m-%d") >= sd]
        if f_end:
            ed = datetime.strptime(f_end, "%Y-%m-%d")
            res = [x for x in res if datetime.strptime(x["date"], "%Y-%m-%d") <= ed]
    except ValueError:
        messagebox.showerror("Фильтр", "Даты в фильтре: ГГГГ-ММ-ДД")
        return
    refresh_ui(res)

expenses = load_data()
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("550x600")

# Блок ввода
f_add = tk.LabelFrame(root, text="Новый расход", padx=5, pady=5)
f_add.pack(fill="x", padx=10)

tk.Label(f_add, text="Сумма:").grid(row=0, column=0)
ent_amount = tk.Entry(f_add, width=10)
ent_amount.grid(row=0, column=1)

tk.Label(f_add, text="Категория:").grid(row=0, column=2)
cats = ["Еда", "Транспорт", "Досуг", "Связь", "Другое"]
cb_cat = ttk.Combobox(f_add, values=cats, width=12, state="readonly")
cb_cat.grid(row=0, column=3)

tk.Label(f_add, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0)
ent_date = tk.Entry(f_add, width=15)
ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
ent_date.grid(row=1, column=1, columnspan=2)

tk.Button(f_add, text="Добавить", command=add_entry, width=10).grid(row=1, column=3)

# Блок фильтра
f_search = tk.LabelFrame(root, text="Фильтр", padx=5, pady=5)
f_search.pack(fill="x", padx=10, pady=5)

cb_f_cat = ttk.Combobox(f_search, values=["Все"] + cats, width=10, state="readonly")
cb_f_cat.current(0)
cb_f_cat.grid(row=0, column=0)

ent_f_start = tk.Entry(f_search, width=11); ent_f_start.grid(row=0, column=1)
ent_f_end = tk.Entry(f_search, width=11); ent_f_end.grid(row=0, column=2)
tk.Button(f_search, text="Применить", command=apply_filters).grid(row=0, column=3)

# Таблица
tree = ttk.Treeview(root, columns=("d", "c", "a"), show="headings", height=12)
tree.heading("d", text="Дата"); tree.heading("c", text="Категория"); tree.heading("a", text="Сумма")
tree.pack(padx=10, pady=5, fill="both")

lbl_total = tk.Label(root, text="Итого за период: 0.00", font=("Arial", 11, "bold"))
lbl_total.pack(pady=5)

refresh_ui(expenses)
root.mainloop()
