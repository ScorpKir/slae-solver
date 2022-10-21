from numpy import array


def read_from_file(filepath: str):
    with open(filepath) as f:
        matrix = [list(map(float, row.split(' '))) for row in f.readlines()]
    return matrix


def validate_matrix(matrix: list, dimension: int):
    if dimension != len(matrix):
        print(f'dim: {dimension} len: {len(matrix)}')
        return False
    for row in matrix:
        if len(row) != dimension + 1:
            print(f'dim: {dimension} len: {len(matrix)}')
            return False
        for column in row:
            try:
                float(column)
            except ValueError:
                return False
    return True
