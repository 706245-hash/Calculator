import tkinter as tk
import math
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage

class ToolTip:
    def __init__(self, widget, text_func):
        self.widget = widget
        self.text_func = text_func  # Now accepts a function
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip, 
            text=self.text_func(),  # Call the function to get current text
            justify='left',
            background="#ffffe0", 
            relief='solid', 
            borderwidth=1,
            padx=5,
            pady=5,
            font=('Arial', 10)
        )
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.resizable(0, 0)
        
        # Initialize variables
        self.memory = 0
        self.history = []
        self.current_expression = ""
        self.last_result = ""
        self.trig_mode = "rad"  # 'rad' or 'deg'
        
        # Create display frame
        self.create_display()
        
        # Set focus to display initially
        self.display.focus_set()

        # Make display not selectable
        self.display.configure(insertwidth=0, highlightthickness=0)

        # Create buttons
        self.create_buttons()
        
        # Configure grid weights
        self.configure_grid()
        
        # Add keyboard support
        self.setup_keyboard_bindings()

        # Set the window icon
        self.set_window_icon()

    def set_window_icon(self):
        """Attempt to set window icon using multiple methods"""
        icon_paths = [
            'assets/icon.ico',
            'assets/calc.jpg'
        ]
        
        for icon_path in icon_paths:
            try:
                # Try Windows .ico method first
                self.root.iconbitmap(icon_path)
                return
            except:
                try:
                    # Try cross-platform method
                    img = PhotoImage(file=icon_path)
                    self.root.tk.call('wm', 'iconphoto', self.root._w, img)
                    return
                except:
                    continue

    def create_display(self):
        # Main display
        self.display = tk.Entry(
            self.root, 
            width=30, 
            font=('Arial', 18), 
            borderwidth=5, 
            justify='right',
            bg='#f5f5f5',
            highlightbackground='gray',
            highlightcolor='gray',
            highlightthickness=1
        )
        self.display.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="ew")
        
        # History display
        self.history_label = tk.Label(
            self.root,
            text="History:",
            font=('Arial', 10),
            anchor='w'
        )
        self.history_label.grid(row=1, column=0, columnspan=6, sticky="w", padx=10)
        
        self.history_display = tk.Listbox(
            self.root,
            height=5,
            font=('Arial', 10),
            selectbackground='#d9d9d9'
        )
        self.history_display.grid(row=2, column=0, columnspan=6, padx=10, pady=5, sticky="ew")
        
        # Allow history display to receive focus but pass keys to root
        self.history_display.bind('<Key>', lambda e: self.root.focus_set())

        # Mode indicator
        self.mode_label = tk.Label(
            self.root,
            text=f"Mode: {self.trig_mode.upper()}",
            font=('Arial', 10),
            anchor='e'
        )
        self.mode_label.grid(row=1, column=4, columnspan=2, sticky="e", padx=10)
    
    def create_buttons(self):
        # Button layout with tooltip text
        button_info = [
            # Text, Tooltip, Row, Column
            ('MC', 'Memory Clear (Ctrl+M)', 3, 0),
            ('MR', 'Memory Recall (Ctrl+R)', 3, 1),
            ('M+', 'Memory Add (Ctrl++)', 3, 2),
            ('M-', 'Memory Subtract (Ctrl+-)', 3, 3),
            ('MS', 'Memory Store (Ctrl+S)', 3, 4),
            ('⌫', 'Backspace (Backspace)', 3, 5),
            
            ('sin', f'sine (s) - Current mode: {self.trig_mode}', 4, 0),
            ('cos', f'cosine (c) - Current mode: {self.trig_mode}', 4, 1),
            ('tan', f'tangent (t) - Current mode: {self.trig_mode}', 4, 2),
            ('log', 'logarithm base 10 (l)', 4, 3),
            ('ln', 'natural logarithm (n)', 4, 4),
            ('Mod', 'modulo (m)', 5, 5),
            
            ('(', 'left parenthesis (()', 5, 0),
            (')', 'right parenthesis ())', 5, 1),
            ('xʸ', 'power (^ or xʸ)', 8, 4),
            ('/', 'divide (/)', 6, 3),
            ('π', 'pi (p)', 5, 4),
            ('n!', 'factorial (!)', 5, 3),
            
            ('7', '7', 6, 0),
            ('8', '8', 6, 1),
            ('9', '9', 6, 2),
            ('*', 'multiply (*)', 7, 3),
            ('√', 'square root (q)', 6, 4),
            ('C', 'clear (Esc)', 4, 5),
            
            ('4', '4', 7, 0),
            ('5', '5', 7, 1),
            ('6', '6', 7, 2),
            ('-', 'subtract (-)', 8, 3),
            ('10ˣ', '10 to power of x', 7, 4),
            ('eˣ', 'e to power of x (e)', 7, 5),
            
            ('1', '1', 8, 0),
            ('2', '2', 8, 1),
            ('3', '3', 8, 2),
            ('+', 'add (+)', 9, 3),
            ('ⁿ√', 'nth root (r)', 6, 5),
            ('|x|', 'absolute value', 8, 5),
            
            ('0', '0', 9, 1),
            ('.', 'decimal point (.)', 9, 2),
            ('D/R', 'toggle degree/radian mode (d)', 5, 2),
            ('+/-', 'toggle sign', 9, 0),
            ('1/x', 'reciprocal', 9, 4),
            ('=', 'equals (Enter)', 9, 5)
        ]
        
        # Button colors
        button_colors = {
            'numbers': '#f0f0f0',
            'operators': '#e6e6e6',
            'equals': '#99ccff',
            'clear': '#ff9999',
            'memory': '#ccffff',
            'scientific': '#e6ccff',
            'special': '#ffe6cc'
        }
        
        # Create buttons with tooltips
        for text, tooltip_text, row, col in button_info:
            # Determine button color
            if text.isdigit() or text == '.':
                bg = button_colors['numbers']
            elif text in ['+', '-', '*', '/', '(', ')', '+/-']:
                bg = button_colors['operators']
            elif text == '=':
                bg = button_colors['equals']
            elif text in ['C', '⌫']:
                bg = button_colors['clear']
            elif text in ['MC', 'MR', 'M+', 'M-', 'MS']:
                bg = button_colors['memory']
            elif text in ['sin', 'cos', 'tan', 'log', 'ln', '√', 'xʸ', 'n!', 'π', 
                        'Mod', '10ˣ', 'eˣ', 'x²', '1/x', '|x|','ⁿ√', 'D/R']:
                bg = button_colors['scientific']
            else:
                bg = button_colors['special']
            
            # Create button
            btn = tk.Button(
                self.root,
                text=text,
                padx=10,
                pady=10,
                command=lambda t=text: self.on_button_click(t),
                bg=bg,
                relief=tk.RIDGE,
                borderwidth=2
            )

            if text in ['sin', 'cos', 'tan']:
                # Use lambda to capture current mode
                tooltip_func = lambda t=text: f"{t} - Current mode: {self.trig_mode.upper()}"
                setattr(self, f'{text}_tooltip', ToolTip(btn, tooltip_func))
            else:
                setattr(self, f'{text}_tooltip', ToolTip(btn, lambda t=tooltip_text: t))

            btn.grid(row=row, column=col, sticky="nsew")
    
    def configure_grid(self):
        # Configure row and column weights
        for i in range(10):  # Enough rows for all elements
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(6):   # 6 columns
            self.root.grid_columnconfigure(i, weight=1)
    
    def setup_keyboard_bindings(self):
        # Number keys
        for num in range(10):
            self.root.bind(str(num), lambda event, n=str(num): self.on_button_click(n))
            self.display.bind(str(num), lambda event, n=str(num): self.on_button_click(n))
        
        # Operation keys - use keysym instead of keycode for better compatibility
        key_mappings = {
            'plus': '+',
            'minus': '-',
            'asterisk': '*',
            'slash': '/',
            'Return': '=',
            'BackSpace': '⌫',
            'Escape': 'C',
            'period': '.',
            'parenleft': '(',
            'parenright': ')',
            'asciicircum': 'xʸ',
            'exclam': 'n!',
            'm': 'Mod',
            's': 'sin',
            'c': 'cos',
            't': 'tan',
            'l': 'log',
            'n': 'ln',
            'q': '√',
            'p': 'π',
            'e': 'eˣ',
            'd': 'D/R',
            'r': 'ⁿ√',
            'percent': 'Mod'
        }
        
        for key, value in key_mappings.items():
            self.root.bind(f'<{key}>', lambda event, v=value: self.on_button_click(v))
            self.display.bind(f'<{key}>', lambda event, v=value: self.on_button_click(v))
        
        # Numpad keys
        numpad_mappings = {
            'KP_Add': '+',
            'KP_Subtract': '-',
            'KP_Multiply': '*',
            'KP_Divide': '/',
            'KP_Enter': '=',
            'KP_Decimal': '.',
            'KP_0': '0',
            'KP_1': '1',
            'KP_2': '2',
            'KP_3': '3',
            'KP_4': '4',
            'KP_5': '5',
            'KP_6': '6',
            'KP_7': '7',
            'KP_8': '8',
            'KP_9': '9'
        }
        
        for key, value in numpad_mappings.items():
            self.root.bind(f'<{key}>', lambda event, v=value: self.on_button_click(v))
            self.display.bind(f'<{key}>', lambda event, v=value: self.on_button_click(v))
        
        # Memory operation shortcuts
        mem_mappings = {
            'Control-m': 'MC',
            'Control-r': 'MR',
            'Control-plus': 'M+',
            'Control-minus': 'M-',
            'Control-s': 'MS'
        }
        
        for key, value in mem_mappings.items():
            self.root.bind(f'<{key}>', lambda event, v=value: self.on_button_click(v))
            self.display.bind(f'<{key}>', lambda event, v=value: self.on_button_click(v))
        
        # Handle focus properly
        self.display.bind('<FocusIn>', self.handle_display_focus)
        self.display.bind('<FocusOut>', self.handle_display_focus_out)
        
        # Set initial focus
        self.display.focus_set()

    def handle_display_focus(self, event=None):
        # When display gets focus, ensure keyboard input works
        self.display.configure(highlightbackground='blue', highlightcolor='blue')
        self.root.focus_set()  # Keep root window focused for key bindings

    def handle_display_focus_out(self, event=None):
        # Visual feedback when display loses focus
        self.display.configure(highlightbackground='gray', highlightcolor='gray')
    
    def on_button_click(self, button_text):
        current_display = self.display.get()
        
        # Clear error if present when new input starts
        if current_display == "Error":
            self.clear_display()
            current_display = ""

        try:
            # Handle function buttons with auto-completion
            function_map = {
                'sin': 'math.sin(',
                'cos': 'math.cos(',
                'tan': 'math.tan(',
                'log': 'math.log10(',
                'ln': 'math.log(',
                '√': 'math.sqrt(',
                'eˣ': 'math.exp(',
                '|x|': 'abs('
            }
            
            if button_text in function_map:
                self.display.insert(tk.END, function_map[button_text])
                return
                
            if button_text.isdigit() or button_text == '.':
                self.handle_digit_or_decimal(button_text)
            elif button_text in ['+', '-', '*', '/', '(', ')']:
                self.handle_operator(button_text)
            elif button_text == '=':
                self.calculate_result()
            elif button_text == 'C':
                self.clear_display()
            elif button_text == '⌫':
                self.backspace()
            elif button_text == '+/-':
                self.toggle_sign()
            elif button_text in ['sin', 'cos', 'tan']:
                self.handle_trig_function(button_text)
            elif button_text == 'xʸ':
                if current_display and not current_display.strip().endswith(('+', '-', '*', '/', '(')):
                    self.display.insert(tk.END, '**')
                else:
                    raise ValueError("Missing base for power operation")
            elif button_text == 'n!':
                self.handle_factorial()
            elif button_text == 'π':
                self.display.insert(tk.END, 'math.pi')
            elif button_text == 'Mod':
                self.display.insert(tk.END, '%')
            elif button_text == '10ˣ':
                self.display.insert(tk.END, '10**')
            elif button_text == 'x²':
                self.display.insert(tk.END, '**2')
            elif button_text == '1/x':
                self.handle_reciprocal()
            elif button_text == 'D/R':
                self.toggle_trig_mode()
            elif button_text in ['MC', 'MR', 'M+', 'M-', 'MS']:
                self.handle_memory_operations(button_text)
            elif button_text == 'ⁿ√':
                self.handle_nth_root()
            
            # Update current expression
            self.current_expression = self.display.get()
            
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
    
    def handle_digit_or_decimal(self, char):
        # Clear error if present
        if self.display.get() == "Error":
            self.clear_display()

        # If last result is displayed and user starts typing a number, clear first
        if self.last_result and self.display.get() == self.last_result:
            self.display.delete(0, tk.END)
            self.last_result = ""
        
        # Handle decimal point
        if char == '.':
            current = self.display.get()
            # Check if current number already has a decimal point
            if '.' not in current.split()[-1] if current else True:
                self.display.insert(tk.END, char)
        else:
            self.display.insert(tk.END, char)
    
    def handle_operator(self, operator):
        # Clear error if present
        if self.display.get() == "Error":
            self.clear_display()

        # If last result is displayed and user presses an operator, use it as first operand
        if self.last_result and self.display.get() == self.last_result:
            self.display.insert(tk.END, operator)
            self.last_result = ""
        else:
            self.display.insert(tk.END, operator)
    
    def is_valid_expression(self, expr):
        """Check if expression is mathematically valid"""
        try:
            # Check for balanced parentheses
            if expr.count('(') != expr.count(')'):
                return False
                
            # Check for consecutive operators (but allow ** as power operator)
            operators = '+-*/%'
            expr = expr.replace('**', '@')  # Temporary replace ** with @
            
            for i in range(len(expr)-1):
                if expr[i] in operators and expr[i+1] in operators:
                    return False
                    
            return True
        except:
            return False

    def validate_before_calculation(self):
        """Validate expression before calculation"""
        expr = self.display.get()
        if not expr:
            raise ValueError("Empty expression")
        if not self.is_valid_expression(expr):
            raise ValueError("Invalid expression format")

    def safe_eval(self, expression):
        """Safely evaluate mathematical expressions"""
        allowed_names = {
            'math': math,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'sqrt': math.sqrt,
            'exp': math.exp,
            'abs': abs,
            'pi': math.pi,
            'e': math.e
        }
        
        try:
            # Replace ^ with ** for power operation
            expression = expression.replace('^', '**')
            
            # Handle empty parentheses cases
            expression = expression.replace('()', '(0)')
            
            # Check for potentially dangerous operations
            if '__' in expression or ';' in expression:
                raise ValueError("Invalid expression")
                
            # Compile first to check syntax
            code = compile(expression, '<string>', 'eval')
            
            # Check for disallowed operations
            for name in code.co_names:
                if name not in allowed_names:
                    raise ValueError(f"Use of '{name}' not allowed")
                    
            return eval(code, {'__builtins__': {}}, allowed_names)
        except Exception as e:
            raise ValueError(f"Evaluation error: {str(e)}")

    def show_error(self, message):
        """Display error message in a user-friendly way"""
        self.display.delete(0, tk.END)
        self.display.insert(0, "Error")
        messagebox.showerror("Calculation Error", message)

    def calculate_result(self):
        try:
            expression = self.display.get()
            if not expression:
                raise ValueError("Empty expression")
                
            # Add closing parentheses if needed
            open_paren = expression.count('(')
            close_paren = expression.count(')')
            while open_paren > close_paren:
                expression += ')'
                close_paren += 1
                
            # Validate the expression
            if not self.is_valid_expression(expression):
                raise ValueError("Invalid expression format")
                
            expression = expression.replace('×', '*').replace('÷', '/')
            
            result = self.safe_eval(expression)
            
            # Format result
            if isinstance(result, float):
                result = round(result, 10) if not result.is_integer() else int(result)
            
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.history.append(f"{expression} = {result}")
            self.update_history_display()
            self.last_result = str(result)
            
        except Exception as e:
            self.show_error(str(e))
    
    def clear_display(self):
        self.display.delete(0, tk.END)
        self.last_result = ""
    
    def backspace(self):
        current = self.display.get()
        if current:
            self.display.delete(len(current)-1, tk.END)
    
    def toggle_sign(self):
        current = self.display.get()
        if current:
            if current[0] == '-':
                self.display.delete(0)
            else:
                self.display.insert(0, '-')
    
    def handle_trig_function(self, func):
        if self.trig_mode == "deg":
            self.display.insert(tk.END, f'math.{func}(math.radians(')
        else:
            self.display.insert(tk.END, f'math.{func}(')
        
    def handle_factorial(self):
        try:
            current = self.display.get()
            if not current:
                raise ValueError("No input for factorial")
                
            num = self.safe_eval(current)
            
            if num < 0:
                raise ValueError("Factorial of negative number")
            if num > 1000:
                raise ValueError("Number too large for factorial")
                
            # Use gamma function for non-integers
            if not float(num).is_integer():
                result = math.gamma(num + 1)
            else:
                result = math.factorial(int(num))
                
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            
        except ValueError as ve:
            self.show_error(str(ve))
        except Exception:
            self.show_error("Factorial calculation failed")
    

    def handle_nth_root(self):
        current = self.display.get()
        if not current:
            # If empty, just insert the root function
            self.display.insert(tk.END, '**(1/')
        else:
            # If there's content, wrap it in parentheses and add root
            self.display.insert(0, '(')
            self.display.insert(tk.END, ')**(1/')

    def toggle_trig_mode(self):
        self.trig_mode = "deg" if self.trig_mode == "rad" else "rad"
        self.mode_label.config(text=f"Mode: {self.trig_mode.upper()}")
        
        # Flash the mode label to draw attention
        self.mode_label.config(bg='yellow')
        self.root.after(200, lambda: self.mode_label.config(bg=self.root.cget('bg')))
        
        # Force tooltip updates by hiding existing ones
        for func in ['sin', 'cos', 'tan']:
            if hasattr(self, f'{func}_tooltip'):
                getattr(self, f'{func}_tooltip').hide_tooltip()
    
    def handle_memory_operations(self, operation):
        try:
            current = self.display.get()
            value = self.safe_eval(current) if current else 0
            
            if operation == 'MC':
                self.memory = 0
            elif operation == 'MR':
                self.display.delete(0, tk.END)
                self.display.insert(0, str(self.memory))
            elif operation == 'M+':
                self.memory += value
            elif operation == 'M-':
                self.memory -= value
            elif operation == 'MS':
                self.memory = value
            
            # Show memory stored notification
            if operation != 'MR':
                messagebox.showinfo("Memory", f"Memory {operation}: {self.memory}")
        
        except ValueError as ve:
            self.show_error(f"Memory operation failed: {str(ve)}")
        except Exception:
            self.show_error("Memory operation failed")
    
    def update_history_display(self):
        self.history_display.delete(0, tk.END)
        for item in reversed(self.history[-5:]):  # Show last 5 items
            self.history_display.insert(0, item)

# Create and run the calculator
if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()