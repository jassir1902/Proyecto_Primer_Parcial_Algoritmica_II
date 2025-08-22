# Fibonacci sequence using recursion
def fibonacci(n):
    # First base case
    if n == 0:
        return 0
    # Second base case
    if n == 1:
        return 1
    # Recursive step
    return fibonacci(n - 1) + fibonacci(n - 2)

# Example usage
# print(fibonacci(10))