def sumar_pares_con_for(limite_superior):
    suma_total = 0
    for numero in range(limite_superior):
        if numero % 2 == 0:
            suma_total = suma_total + numero
    return suma_total