# Scientific Calculator with Tkinter

![Calculator Screenshot](calculator/assets/calc.png) 
*(Calculator screenshot)*

A feature-rich scientific calculator built with Python's Tkinter GUI toolkit, offering both basic and advanced mathematical operations with an intuitive interface.

## Features

### Core Functionality
- **Basic Operations**: Addition, subtraction, multiplication, division
- **Scientific Functions**:
  - Trigonometric (sin, cos, tan) with DEG/RAD mode toggle
  - Logarithmic (log10, ln)
  - Power functions (xʸ, x², 10ˣ, eˣ)
  - Square root (√), absolute value (|x|)
  - Factorial (n!), reciprocal (1/x)
  - Modulo (Mod) operations
- **Memory Operations**: MC, MR, M+, M-, MS
- **Constants**: π (pi), e

### Enhanced UI Features
- **Interactive Tooltips**: Hover over any button to see its function and keyboard shortcut
- **Calculation History**: View last 5 calculations
- **Color-coded Buttons**: Different colors for numbers, operations, and functions
- **DEG/RAD Mode Indicator**: Shows current trigonometric mode

### Keyboard Support
Full keyboard support with shortcuts for all operations:
- Numbers: `0-9`
- Basic operations: `+`, `-`, `*`, `/`
- Scientific functions: 
  - `s` for sin, `c` for cos, `t` for tan
  - `l` for log, `n` for ln
  - `q` for square root, `^` for power
  - `!` for factorial, `m` for modulo
- Navigation: `Enter` (=), `Backspace` (⌫), `Esc` (C)

## Installation

1. **Prerequisites**:
   - Python 3.6 or higher
   - Tkinter (usually included with Python)

2. **Running the Calculator**:
   ```bash
   git clone https://github.com/706245-hash/Calculator.git
   cd tkinter-calculator
   python calculator.py
