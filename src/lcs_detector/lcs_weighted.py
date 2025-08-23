# src/lcs_detector/lcs_weighted.py

def lcs_weighted(seq1, weights1, seq2, weights2):
    """
    Calcula la Subsecuencia Común Más Larga (LCS) ponderada.
    """
    m, n = len(seq1), len(seq2)
    c = [[0.0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                # Pondera usando el promedio de los pesos del token coincidente
                weight = (weights1[i - 1] + weights2[j - 1]) / 2.0
                c[i][j] = c[i - 1][j - 1] + weight
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])
    
    # Reconstrucción de la secuencia LCS
    lcs_sequence = []
    i, j = m, n
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            lcs_sequence.append(seq1[i - 1])
            i -= 1
            j -= 1
        elif c[i - 1][j] >= c[i][j - 1]: i -= 1
        else: j -= 1

    # Cálculo del score de similitud
    weighted_lcs_score = c[m][n]
    total_weight = sum(weights1) + sum(weights2)
    
    if total_weight == 0: return 0.0, []

    similarity = (2 * weighted_lcs_score) / total_weight
    return similarity, lcs_sequence[::-1]