# src/lcs_detector/lcs_weighted.py

def lcs_weighted(seq1, seq2, weights):
    """
    Calcula la Subsecuencia Común Más Larga (LCS) ponderada entre dos secuencias de tokens.
    ...
    """
    m, n = len(seq1), len(seq2)
    
    C = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1][1] == seq2[j - 1][1]:
                C[i][j] = C[i - 1][j - 1] + weights.get(seq1[i - 1][0], 1)
            else:
                C[i][j] = max(C[i - 1][j], C[i][j - 1])

    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if seq1[i - 1][1] == seq2[j - 1][1]:
            lcs.append(seq1[i - 1][1])
            i -= 1
            j -= 1
        elif C[i - 1][j] >= C[i][j - 1]:
            i -= 1
        else:
            j -= 1

    total_seq1 = sum(weights.get(token[0], 1) for token in seq1)
    total_seq2 = sum(weights.get(token[0], 1) for token in seq2)
    
    # Si el peso total de ambas secuencias es 0, la similitud también es 0.
    denominator = total_seq1 + total_seq2
    if denominator == 0:
        score = 0.0
    else:
        score = 2 * C[m][n] / denominator # Fórmula del score de similitud

    return C[m][n], lcs[::-1], score

