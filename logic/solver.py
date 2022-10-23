def bubble_max_row(m, col):
    max_element = m[col][col]
    max_row = col
    for i in range(col + 1, len(m)):
        if abs(m[i][col]) > abs(max_element):
            max_element = m[i][col]
            max_row = i
    if max_row != col:
        m[col], m[max_row] = m[max_row], m[col]


def solve_gauss(m):
    result = ''
    n = len(m)
    # forward trace
    for k in range(n - 1):
        bubble_max_row(m, k)
        for i in range(k + 1, n):
            div = m[i][k] / m[k][k]
            m[i][-1] -= div * m[k][-1]
            for j in range(k, n):
                m[i][j] -= div * m[k][j]

    # check modified system for nonsingularity
    if is_singular(m):
        return 'The system has infinite number of answers...'

    # backward trace
    x = [0 for _ in range(n)]
    for k in range(n - 1, -1, -1):
        x[k] = (m[k][-1] - sum([m[k][j] * x[j] for j in range(k + 1, n)])) / m[k][k]

    for i in range(len(x) - 1):
        result += f'x{i+1} = {x[i]}, '
        result += f'x{len(x)} = {x[len(x) - 1]}'
    return result


def is_singular(m):
    """Check matrix for nonsingularity.
    :param m: matrix (list of lists)
    :return: True if system is nonsingular
    """
    for i in range(len(m)):
        if not m[i][i]:
            return True
    return False
