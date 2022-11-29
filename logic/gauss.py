import numpy as np
from logic.utils import answer_to_string, symmetrize_matrix

def gauss(matrix: np.array) -> np.array:
    '''Функция решает СЛАУ (заданную в виде матрицы) методом Гаусса и взвращает информацию о решении для вывода на экран'''

    result: str = 'Исходная матрица:\n' + str(matrix) + '\n' * 2

    # Обозначаем допустимую погрешность
    TOLERANCE: float = 0.0001

    # Получаем размерность матрицы
    DIMENSION: float = len(matrix)

    # Симметризируем нашу матрицу
    # matrix = symmetrize_matrix(matrix)

    # Зануляем все элементы, находящиеся под главной диагональю
    for col in range(DIMENSION):

        # Выбираем главную строку по максимальному элементу столбца
        pivot: int = col
        for lower_row in range(col, DIMENSION):
            if abs(matrix[lower_row, col]) > abs(matrix[pivot, col]): 
                pivot = lower_row
            
        # Проверяем является ли наш опорный элемент 0 или близким к 0 
        if abs(matrix[pivot, col]) < TOLERANCE:
            continue

        # Если наш опорный элемент таковым не оказался, то поднимаем строку вверх
        for right_column in range(DIMENSION + 1):
            matrix[pivot, right_column], matrix[col, right_column] = matrix[col, right_column], matrix[pivot, right_column]

        # Далее зануляем строки снизу и сверху
        for row in range(DIMENSION):
            if row != col:
                factor: float = matrix[row, col] / matrix[col, col]
                for right_column in range(col, DIMENSION + 1):
                    matrix[row, right_column] -= matrix[col, right_column] * factor

                    # Если полученное значение близко к 0, то приравниваем его к 0 (для простоты вычислений)
                    if abs(matrix[row, right_column]) < TOLERANCE:
                        matrix[row, right_column] = 0.0

    result += 'Матрица после приведения к диагональному виду:\n' + str(matrix) + '\n' + '-' * 50 + '\n' * 2

    # Выясняем решения системы
    answer: np.array = np.zeros(DIMENSION)

    is_inf_solutions: bool = False
    
    # Для каждой переменной находим значение    
    for col in range(DIMENSION):
        if matrix[col][col] == 0.0:
            is_inf_solutions = True
            answer[col] = 0.0
        else:
            answer[col] = matrix[col][DIMENSION] / matrix[col][col]
     
    # Проверяем есть ли решения у системы
    for row in range(DIMENSION):

        # Ищем сумму корней умноженных на коэффиценты
        var_sum: float = sum(list(map(lambda first, second: first * second, answer, matrix[row])))

        # Сравниваем их со свободным членом. Если разница достаточно велика, то решений у системы нет
        if abs(var_sum - matrix[row][DIMENSION]) > TOLERANCE:
            result += 'Система не имеет решений!'
            return result

    if is_inf_solutions:
        result += f'Система имеет бесконечное количество решений\nВот одно из них: {answer_to_string(answer)}'
        return result

    result += f'Решение системы уравнений: {answer_to_string(answer)}'
    return result
