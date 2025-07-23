import tkinter as tk
from tkinter import ttk, messagebox
from modules import helper, BSModel, BTModel, MCModel, Ticker, pop_ticks

def run_models():
    ticker = ticker_var.get()
    try:
        time_to_expiry = int(expiry_var.get())
        risk_free_rate = float(rate_var.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for expiry and risk-free rate.")
        time_to_expiry = 5.0
        risk_free_rate = 5.0

    try:
        option_data = helper.get_option_data(ticker, time_to_expiry)
    except Exception as e:
        messagebox.showerror("Data Error", str(e))
        return

    time_to_expiry = option_data["time_to_expiry"]
    spot_price = option_data["spot_price"]
    volatility = option_data["volatility"]
    strike_prices = option_data["strike_prices"]
    call_prices_real = option_data["calls"]
    put_prices_real = option_data["puts"]

    strike_prices_c = option_data["strike_prices_c"]
    strike_prices_p = option_data["strike_prices_p"]

    call_price_dict = dict(zip(strike_prices_c, call_prices_real))
    put_price_dict = dict(zip(strike_prices_p, put_prices_real))

    # Clear previous table
    for row in tree.get_children():
        tree.delete(row)

    # Insert rows with alternating colours
    for ind, sp in enumerate(strike_prices):
        BSM = BSModel(spot_price, sp, time_to_expiry, risk_free_rate/100.0, volatility)
        BTM = BTModel(spot_price, sp, time_to_expiry, risk_free_rate/100.0, volatility, 30)
        MCM = MCModel(spot_price, sp, time_to_expiry, risk_free_rate/100.0, volatility, 1000)

        call_real = call_price_dict.get(sp, '-')
        call_BSM = BSM.calculate_option_price('Call')
        call_BTM = BTM.calculate_option_price('Call')
        call_MCM = MCM.calculate_option_price('Call')

        put_real = put_price_dict.get(sp, '-')
        put_BSM = BSM.calculate_option_price('Put')
        put_BTM = BTM.calculate_option_price('Put')
        put_MCM = MCM.calculate_option_price('Put')

        tree.insert('', 'end', values=(
            f"{sp:.2f}",
            f"{call_real if call_real == '-' else f'{call_real:.2f}'}", f"{call_BSM:.2f}", f"{call_BTM:.2f}", f"{call_MCM:.2f}",
            f"{put_real if put_real == '-' else f'{put_real:.2f}'}", f"{put_BSM:.2f}", f"{put_BTM:.2f}", f"{put_MCM:.2f}"
        ), tags=('oddrow' if ind % 2 else 'evenrow'))

    result_text.set(
        f"Volatility: {volatility:.4f}\n"
        f"Spot Price: {spot_price:.2f}\n"
        f"Time to Expiry: {time_to_expiry} days\n"
        f"Risk-Free Rate: {risk_free_rate}"
    )

root = tk.Tk()
root.title("Option Pricing Model Comparison")
root.geometry("800x600")
root.resizable(True, True)

style = ttk.Style(root)
style.theme_use('clam')

# Custom colours
BG_COLOR = "#e3f2fd"
TITLE_COLOR = "#1565c0"
LABEL_COLOR = "#0d47a1"
ENTRY_BG = "#ffffff"
BUTTON_BG = "#42a5f5"
BUTTON_FG = "#ffffff"
EVEN_ROW = "#bbdefb"
ODD_ROW = "#e3f2fd"

frame = ttk.Frame(root, padding=20)
frame.pack(fill=tk.BOTH, expand=True)
frame.configure(style="Main.TFrame")

# Title
title_label = tk.Label(frame, text="Option Pricing", font=("Arial", 24, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")

# Input labels and entries
ttk.Label(frame, text="Ticker Name:", font=("Arial", 12, "bold"), foreground=LABEL_COLOR, background=BG_COLOR).grid(row=1, column=0, sticky="w")
ticker_var = tk.StringVar()
ticker_entry = ttk.Combobox(frame, textvariable=ticker_var, font=("Arial", 12), values=pop_ticks.POPULAR_TICKERS)
ticker_entry.grid(row=1, column=1, pady=5, sticky="ew")
ticker_entry.set('')  # Start with empty

ttk.Label(frame, text="Time to Expiry (days):", font=("Arial", 12, "bold"), foreground=LABEL_COLOR, background=BG_COLOR).grid(row=2, column=0, sticky="w")
expiry_var = tk.StringVar()
expiry_entry = ttk.Entry(frame, textvariable=expiry_var, font=("Arial", 12))
expiry_entry.grid(row=2, column=1, pady=5, sticky="ew")

ttk.Label(frame, text="Risk-Free Rate (%):", font=("Arial", 12, "bold"), foreground=LABEL_COLOR, background=BG_COLOR).grid(row=3, column=0, sticky="w")
rate_var = tk.StringVar()
rate_entry = ttk.Entry(frame, textvariable=rate_var, font=("Arial", 12))
rate_entry.grid(row=3, column=1, pady=5, sticky="ew")

# Button
run_button = tk.Button(frame, text="Run Models", command=run_models, font=("Arial", 12, "bold"),
                       bg=BUTTON_BG, fg=BUTTON_FG, activebackground=LABEL_COLOR, activeforeground=BUTTON_FG)
run_button.grid(row=4, column=0, columnspan=2, pady=15, ipadx=10, ipady=2)

# Result box 
result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, font=("Arial", 9), background="#f5f5f5",
                        anchor="nw", justify="left", height=3, width=40, relief="groove", bd=2)
result_label.grid(row=5, column=0, columnspan=2, sticky="nw", pady=5)

columns = (
    "Strike", "Call Real", "Call Black-Scholes", "Call Binomial Tree", "Call Monte Carlo",
    "Put Real", "Put Black-Scholes", "Put Binomial Tree", "Put Monte Carlo"
)
style = ttk.Style(root)
style.theme_use('clam')
style.configure("Treeview.Heading", font=("Arial", 13, "bold"))
style.configure("Treeview", font=("Arial", 12))

tree = ttk.Treeview(frame, columns=columns, show='headings', height=18)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=85)
tree.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

# Add row tags for colouring
tree.tag_configure('evenrow', background=EVEN_ROW)
tree.tag_configure('oddrow', background=ODD_ROW)

frame.rowconfigure(6, weight=1)
frame.columnconfigure(1, weight=1)

# Set background colour for frame and root
frame.configure(style="Main.TFrame")
style.configure("Main.TFrame", background=BG_COLOR)
root.configure(bg=BG_COLOR)

root.mainloop()