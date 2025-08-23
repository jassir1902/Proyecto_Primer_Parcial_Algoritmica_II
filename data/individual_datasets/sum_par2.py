def calcular_suma_pares_con_while(n):
    total = 0
    contador = 0
    while contador < n:
        if contador % 2 == 0:
            total += contador
        contador += 1
    return total