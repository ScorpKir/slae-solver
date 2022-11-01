def read_from_file(filepath: str):
    with open(filepath) as f:
        matrix = [list(map(float, row.split(' '))) for row in f.readlines()]
    return matrix


def validate_matrix(matrix: list, dimension: int):
    '''Функция осуществляет валидацию полученной матрицы по критериям соответствия размерности и корректности значений'''

    # Если введенная матрица не соотвесттвует размерности, то она введена неверно
    if dimension != len(matrix):
        return False
    for row in matrix:
        if len(row) != dimension + 1:
            return False
        
        # Если значение полученной матрицы нельзя привести к типу float, то в матрице присутствует некорректное значение
        for column in row:
            try:
                float(column)
            except ValueError:
                return False
    
    # Если выход из функции не произошёл, то матрица введена корректно
    return True
