import tkinter as tk
from tkinter import messagebox

def get_valid_number(entry_widget):
    try:
        return float(entry_widget.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid number!")
        return None

def calculate(operation):
    num1 = get_valid_number(entry_num1)
    num2 = get_valid_number(entry_num2)

    if num1 is None or num2 is None:
        return
    
    operations = {
        "add" : num1 + num2,
        "subtract" : num1 - num2,
        "multiply" : num1 * num2,
        "divide" : num1 / num2 if num2 !=0 else "Error: Division by zero!"
    }

    result = operations.get(operation, "Invalid operation")
    label_result.config(text = f"Result: {result}")

#Main window creation
root = tk.Tk()
root.title("Simple Calculator")

#Input fields
tk.Label(root, text = "First Number:").pack()
entry_num1 = tk.Entry(root)
entry_num1.pack()

tk.Label(root, text = "Second Number:").pack()
entry_num2 = tk.Entry(root)
entry_num2.pack()

#Operation buttons
tk.Button(root, text="Add", command=lambda: calculate("add")).pack()
tk.Button(root, text="Subtract", command=lambda: calculate("subtract")).pack()
tk.Button(root, text="Multiply", command=lambda: calculate("multiply")).pack()
tk.Button(root, text="Divide", command=lambda: calculate("divide")).pack()

#Result display
label_result = tk.Label(root, text="Result: ")
label_result.pack()

#Run the app
root.mainloop()