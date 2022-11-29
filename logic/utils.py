import numpy as np

def answer_to_string(answer: np.array) -> str:
    '''Функция переводит массив с решением СЛАУ в строку для вывода на экран'''

    if answer is not None:
        result: str = '| '
        for var, value in enumerate(answer):
            result += f'x{var + 1} = {round(value, 5)} | '
        return result
    return 'Решения не были найдены'
    
def vector_to_string(vector: np.array) -> str:
    '''Функция переводит вектор невязки в строку для вывода на экран или в файл'''

    result: str = '('
    for var, value in enumerate(vector):
        result += f'{round(value, 5)}; '
    result = result[:-2] + ')'
    return result
    
def symmetrize_matrix(matrix: np.array) -> np.array:
    '''Функция применяет симметризацию Гаусса к СЛАУ в виде матрицы'''

    # Столбец свободных членов
    free_odds: np.array = matrix[:, -1]

    # Отрезаем столбец свободных членов от матрицы
    matrix = matrix[:, 0:-1]

    # Транспонированная матрица коэффициентов
    transp_matrix: np.array = np.transpose(matrix)

    # Умножаем столбец свободных членов и матрицу коэффициентов на транспонированную матрицу коэффициентов
    free_odds = np.dot(free_odds, transp_matrix)
    matrix = np.dot(matrix, transp_matrix)

    # Возващаем соединенную симметризированную матрицу коэффициентов и свободных членов
    matrix = np.c_[matrix, free_odds]
    return matrix
