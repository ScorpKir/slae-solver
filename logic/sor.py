import numpy as np
from logic.utils import answer_to_string

def sor(matrix: np.array) -> np.array:
    '''Функция решает СЛАУ (заданную в виде матрицы) методом релаксации'''

    # Допустимая погрешность и параметр релаксации
    TOLERANCE: float = 0.001 
    OMEGA: float = 0.5

    # Размерность системы уравнений и столбец свободных членов
    DIMENSION: int = len(matrix)
    FREE_ODDS: np.array = matrix[:,-1]

    # Удаляем столбец свободных членов из полученной матрицы
    matrix = matrix[:, 0 : -1]
    
    # Счетчик шагов и максимальное количество шагов
    step: int = 0
    MAX_STEPS: int = 1000

    # Самый первый вектор невязки
    guess: np.array = np.zeros(DIMENSION)

    # Суммарная ошибка на нулевом шаге
    residual = np.linalg.norm(np.dot(matrix, guess) - FREE_ODDS)

    # Выполняем итерации пока суммарная ошибка больше допустимой и пока не достигнут предел итераций
    while residual > TOLERANCE and step < MAX_STEPS:
        
        # Для каждой переменной считаем сумму на текущей итерации
        for var in range(DIMENSION):
            sigma: float = 0
            for other_var in range(DIMENSION):
                if var != other_var:
                    sigma += matrix[var, other_var] * guess[other_var]

            # По формуле вычисляем значение переменной на текущей итерации
            guess[var] = (1 - OMEGA) * guess[var] + (OMEGA / matrix[var, var]) * (FREE_ODDS[var] - sigma)

        # Вычисляем суммарную ошибку
        residual = np.linalg.norm(np.dot(matrix, guess) - FREE_ODDS)

        # Увеличиваем шаг
        step += 1

    # Если итерации превысили предел итераций, то ответ не нашелся
    if residual > TOLERANCE:
        return None

    # Иначе возвращаем ответ
    return guess

def solve_sor(matrix: np.array) -> str:
    return answer_to_string(sor(matrix))
