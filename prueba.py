import math

# Utiliza palabras reservadas: import, def, if, else, while, for, try, except, finally, raise
def calculate_factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0:
        return 1
    else:
        result = 1
        while n > 1:
            result *= n
            n -= 1
        return result

def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        sequence = [0, 1]
        for i in range(2, n):
            next_value = sequence[-1] + sequence[-2]
            sequence.append(next_value)
        return sequence

class Calculator:
    def __init__(self):
        self.value = 0
    
    def add(self, x):
        self.value += x
        return self.value
    
    def subtract(self, x):
        self.value -= x
        return self.value
    
    def multiply(self, x):
        self.value *= x
        return self.value
    
    def divide(self, x):
        try:
            self.value /= x
        except ZeroDivisionError:
            print("Error: Division by zero is not allowed")
        return self.value

def main():
    calc = Calculator()
    print("Initial value:", calc.value)
    
    print("Adding 10:", calc.add(10))
    print("Subtracting 5:", calc.subtract(5))
    print("Multiplying by 3:", calc.multiply(3))
    
    # Using the divide method which includes exception handling
    print("Dividing by 2:", calc.divide(2))
    print("Dividing by 0:", calc.divide(0))
    
    # Using functions to calculate factorial and fibonacci
    try:
        num = 5
        print(f"Factorial of {num}:", calculate_factorial(num))
        
        num = 7
        print(f"Fibonacci sequence of length {num}:", fibonacci(num))
    except ValueError as e:
        print("Caught an error:", e)
    
    # Additional uses of reserved keywords
    x = lambda a: a * a
    print("Lambda function result:", x(4))
    
    global_value = 10
    def outer_function():
        global global_value
        global_value = 20
        print("Global value inside function:", global_value)
    
    outer_function()
    print("Global value outside function:", global_value)
    
    nonlocal_value = 30
    def nested_function():
        nonlocal nonlocal_value
        nonlocal_value += 10
        print("Nonlocal value inside nested function:", nonlocal_value)
    
    nested_function()
    print("Nonlocal value outside nested function:", nonlocal_value)
    
    assert 2 + 2 == 4, "Assertion failed: 2 + 2 should equal 4"

if __name__ == "__main__":
    main()
