import numpy as np
from logic.utils import answer_to_string, print_sor_statistics

def sor(matrix: np.array) -> np.array:
    '''Функция решает СЛАУ (заданную в виде матрицы) методом релаксации'''

    # Допустимая погрешность и параметр релаксации
    TOLERANCE: float = 0.001 
    OMEGA: float = 0.9

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

    # Вектора невязки
    vectors: np.array = [np.append(guess, residual)] 

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

        # Если суммарная ошибка равна бесконечности, то метод не сходится
        if np.isinf(residual):
            return vectors.reshape(-1, DIMENSION + 1)

        # Добавляем вектор невязки в массив
        vectors = np.append(vectors, np.append(guess, residual))

        # Увеличиваем шаг
        step += 1

    return vectors.reshape(-1, DIMENSION + 1)

def solve_sor(matrix: np.array) -> str:
    '''Функция запускает решение СЛАУ и формирует строки для вывода'''

    # Допустимая погрешность
    TOLERANCE: float = 0.001

    # Вектора невязки
    vectors = sor(matrix)

    # Вывод информации по векторам невязки в файл
    print_sor_statistics(vectors)

    # Если ошибка на последнем векторе больше допустимой, то метод не сошелся
    if vectors[-1][-1] > TOLERANCE:
        return 'Метод не сошелся. Информация в файле sor_log.txt' 

    # Если метод сошелся, то формируем строку для вывода
    return answer_to_string(vectors[-1][:-1])
