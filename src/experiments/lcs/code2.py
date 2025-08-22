# Calculates the N-th Fibonacci number
def calcular_fib(num):
    """
    Calculates Fibonacci using a recursive approach.
    """
    # Base case for the recursion
    if num <= 1:
        return num
    
    # The recursive call
    resultado = calcular_fib(num - 1) + calcular_fib(num - 2)
    return resultado

# print(calcular_fib(10))