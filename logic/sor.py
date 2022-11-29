import numpy as np
from logic.utils import answer_to_string, vector_to_string, symmetrize_matrix

def sor(matrix: np.array) -> np.array:
    '''Функция решает СЛАУ (заданную в виде матрицы) методом релаксации и возвращает строку с информацией для вывода на дисплей.'''

    # Допустимая погрешность и параметр релаксации
    TOLERANCE: float = 0.001 
    OMEGA: float = 1.1
    # Размерность системы уравнений и столбец свободных членов
    DIMENSION: int = len(matrix)
    FREE_ODDS: np.array = matrix[:,-1]

    # Удаляем столбец свободных членов из полученной матрицы
    matrix = matrix[:, 0 : -1]

    # Счетчик шагов и максимальное количество шагов
    step: int = 0
    MAX_STEPS: int = 1000

    # Строка ответа
    result: str = 'Результаты решения методом релаксации' + '\n' * 2

    # Самый первый вектор невязки
    guess: np.array = np.zeros(DIMENSION)

    # Суммарная ошибка на нулевом шаге
    residual = np.linalg.norm(np.dot(matrix, guess) - FREE_ODDS)

    # Добавляем начальный вектор в ответ
    result += f'Шаг {step}: {vector_to_string(guess)}. Ошибка = {residual} \n'

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
            result += '-' * 50 + '\n' + 'Метод не сошелся.'  
            return result

        # Увеличиваем шаг
        step += 1

        # Добавляем вектор в ответ
        result += f'Шаг {step}: {vector_to_string(guess)}. Ошибка = {residual} \n'

    # Возвращаем
    result += '-' * 50 + '\n' + f'Метод сошелся за {step} шагов.' + '\n' + f'Решение: {answer_to_string(guess)}.'
    return result
