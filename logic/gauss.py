import numpy as np
from logic.utils import answer_to_string

def gauss(matrix: np.array) -> np.array:
    '''Функция решает СЛАУ (заданную в виде матрицы) методом Гаусса'''

    # Обозначаем допустимую погрешность
    tolerance = 0.0001

    # Получаем размерность матрицы
    dimension = len(matrix)

    # Зануляем все элементы, находящиеся под главной диагональю
    for col in range(dimension):

        # Выбираем главную строку по максимальному элементу столбца
        pivot: int = col
        for lower_row in range(col, dimension):
            if abs(matrix[lower_row, col]) > abs(matrix[pivot, col]): 
                pivot = lower_row
            
        # Проверяем является ли наш опорный элемент 0 или близким к 0 
        if abs(matrix[pivot, col]) < tolerance:
            continue

        # Если наш опорный элемент таковым не оказался, то поднимаем строку вверх
        for right_column in range(dimension + 1):
            matrix[pivot, right_column], matrix[col, right_column] = matrix[col, right_column], matrix[pivot, right_column]

        # Далее зануляем строки снизу и сверху
        for row in range(dimension):
            if row != col:
                factor: float = matrix[row, col] / matrix[col, col]
                for right_column in range(col, dimension + 1):
                    matrix[row, right_column] -= matrix[col, right_column] * factor

                    # Если полученное значение близко к 0, то приравниваем его к 0 (для простоты вычислений)
                    if abs(matrix[row, right_column]) < tolerance:
                        matrix[row, right_column] = 0.0

    # Выясняем решения системы
    answer: np.array = np.zeros(dimension)
    
    # Для каждой переменной находим значение    
    for col in range(dimension):
        if matrix[col][col] == 0.0:
            answer[col] = 0.0
        else:
            answer[col] = matrix[col][dimension] / matrix[col][col]
     
    # Проверяем есть ли решения у системы
    for row in range(dimension):

        # Ищем сумму корней умноженных на коэффиценты
        var_sum: float = sum(list(map(lambda first, second: first * second, answer, matrix[row])))

        # Сравниваем их со свободным членом. Если разница достаточно велика, то решений у системы нет
        if abs(var_sum - matrix[row][dimension]) > tolerance:
            return None
        
    return answer

def solve_gauss(matrix: np.array):
    return answer_to_string(gauss(matrix))
