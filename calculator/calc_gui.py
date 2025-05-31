import tkinter as tk
import math

def create_calculator():
    root = tk.Tk()
    root.title("Calculator")
    root.resizable(0, 0)  # Disable resizing
    
    # Memory variable
    memory = 0
    # Track if we're in the middle of a calculation
    calculation_in_progress = False
    
    # Entry widget to display the calculations
    display = tk.Entry(root, width=20, font=('monospace', 16), borderwidth=5, justify='right')
    display.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

    # Button labels in order
    buttons = [
        'M+', 'M-', 'MR', 'MC', '/',
        '7', '8', '9', 'xʸ', '*',
        '4', '5', '6', '%', '-',
        '1', '2', '3', '( )', '+', 
        '+/-', '0', 'C', '⌫', '=',
    ]

    # Function to handle button clicks
    def button_click(char):
        nonlocal memory, calculation_in_progress
        
        current = display.get()
        
        if char == 'C':
            display.delete(0, tk.END)
            calculation_in_progress = False
        elif char == '⌫':  # Backspace
            display.delete(len(current)-1, tk.END)
        elif char == '+/-':  # Toggle sign
            if current and current[0] == '-':
                display.delete(0)
            else:
                display.insert(0, '-')
        elif char == '()':  # Parentheses
            if '(' not in current or current.count('(') == current.count(')'):
                display.insert(tk.END, '(')
            else:
                display.insert(tk.END, ')')
        elif char == 'xʸ':  # Power function
            display.insert(tk.END, '**')
        elif char == '%':  # Percentage
            try:
                result = eval(current)/100
                display.delete(0, tk.END)
                display.insert(0, str(result))
            except:
                display.delete(0, tk.END)
                display.insert(0, "Error")
        elif char == 'M+':  # Memory add
            try:
                memory += eval(current)
                display.delete(0, tk.END)
            except:
                display.delete(0, tk.END)
                display.insert(0, "Error")
        elif char == 'M-':  # Memory subtract
            try:
                memory -= eval(current)
                display.delete(0, tk.END)
            except:
                display.delete(0, tk.END)
                display.insert(0, "Error")
        elif char == 'MR':  # Memory recall
            display.delete(0, tk.END)
            display.insert(0, str(memory))
        elif char == 'MC':  # Memory clear
            memory = 0
            display.delete(0, tk.END)
        elif char == '=':
            try:
                # Replace × with *, ÷ with / for eval
                expression = current.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                display.delete(0, tk.END)
                display.insert(0, str(result))
                calculation_in_progress = True
            except:
                display.delete(0, tk.END)
                display.insert(0, "Error")
        else:
            # If we just calculated a result and user presses a number, clear first
            if calculation_in_progress and char.isdigit():
                display.delete(0, tk.END)
                calculation_in_progress = False
            display.insert(tk.END, char)

    # Create and place all buttons
    row = 1
    col = 0
    for button in buttons:
        # Create button with different colors for different types
        if button.isdigit():
            btn = tk.Button(root, text=button, padx=20, pady=10, 
                           command=lambda b=button: button_click(b),
                           bg='#f0f0f0')
        elif button in ['C', '⌫', 'MC']:  # Red buttons for clear functions
            btn = tk.Button(root, text=button, padx=20, pady=10, 
                           command=lambda b=button: button_click(b),
                           bg='#ff9999')
        elif button == '=':  # Green button for equals
            btn = tk.Button(root, text=button, padx=20, pady=10, 
                           command=lambda b=button: button_click(b),
                           bg='#99ff99')
        elif button in ['M+', 'M-', 'MR']:  # Blue buttons for memory
            btn = tk.Button(root, text=button, padx=20, pady=10, 
                           command=lambda b=button: button_click(b),
                           bg='#9999ff')
        else:  # Gray buttons for operations
            btn = tk.Button(root, text=button, padx=20, pady=10, 
                           command=lambda b=button: button_click(b),
                           bg='#cccccc')
        
        btn.grid(row=row, column=col, sticky="nsew")
        col += 1
        if col > 4:
            col = 0
            row += 1

    # Configure row and column weights
    for i in range(6):
        root.grid_rowconfigure(i, weight=1)
    for i in range(5):
        root.grid_columnconfigure(i, weight=1)

    return root

# Create and run the calculator
calculator = create_calculator()
calculator.mainloop()