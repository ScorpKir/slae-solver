import numpy as np

def answer_to_string(answer: np.array) -> str:
    if answer is not None:
        result: str = '| '
        for var, value in enumerate(answer):
            result += f'x{var + 1} = {round(value, 2)} | '
        return result
    return 'Решения не были найдены'

def print_sor_statistics(vectors: np.array) -> None:
    file = open('sor_log.txt', 'w+')
    for step, item in enumerate(vectors):
        string = f'Step {step}. Vector: {answer_to_string(item[:-1])}. Residual = {item[-1]} \n'
        file.write(string)
    file.close()
    

def dioganic_predominance(matrix: np.array) -> np.array:
    '''Функция приводит матрицу к диагональному преобладанию'''
    
    # Размерность матрицы
    DIMENSION: int = len(matrix)

    # Столбец свободных членов
    free_odds: np.array = matrix[:,-1]

    # Убираем из матрицы столбец свободных членов
    matrix = matrix[:,0:-1]

    # Получаем матрицу обратную нашей
    inverse_matrix: np.array = np.linalg.inv(matrix)

    # Генерируем матрицу с диагональным преобладанием
    complete_matrix: np.array = np.ones((DIMENSION, DIMENSION))
    for var in range(DIMENSION): 
        complete_matrix[var, var] += 7
    
    # Приводим нашу матрицу к той, что получилась на прошлом шаге
    total = inverse_matrix.dot(complete_matrix)
    matrix = matrix.dot(total)
    free_odds = free_odds.dot(total)

    # Конкатенируем столбец свободных членов к матрице
    return np.c_[matrix, free_odds]