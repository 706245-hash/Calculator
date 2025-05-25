def get_valid_number(prompt):
    while True:
        user_input = input(prompt)
        try:
            return int(user_input)
        except ValueError:
            print(f"'{user_input}' is not a valid number. Please try again.")

def calculate(operation):
    operations = {
        "add": lambda a, b: a + b,
        "subtract": lambda a, b: a - b,
        "multiply": lambda a, b: a * b,
        "divide": lambda a, b: a / b if b != 0 else "Error: Division by zero!"
    }
    
    print(f"Enter two numbers to {operation}.")
    num1 = get_valid_number("First number: ")
    num2 = get_valid_number("Second number: ")
    
    result = operations[operation](num1, num2)
    print(f"The result is: {result}")

def main():
    while True:
        print("\nCalculator Menu:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")
        
        choice = input("Choose an operation (1-5): ")
        
        if choice == "1":
            calculate("add")
        elif choice == "2":
            calculate("subtract")
        elif choice == "3":
            calculate("multiply")
        elif choice == "4":
            calculate("divide")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()