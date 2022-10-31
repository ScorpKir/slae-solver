def solve_relaxation(matrix: list):
    '''Функция решает СЛАУ (заданную в виде матрицы) методом релаксации'''
    
    result = 'Вектора невязки: \n'

    # Обозначаем допустиму поэлементную разницу в приближениях
    EPS = 0.0001

    # Получаем размерность исходной матрицы
    dimension: int = len(matrix)

    # Обозначаем параметр релаксации
    PARAMETER = 0.5

    # Инициализируем самый первый вектор невязки
    previous_approx = [0 for _ in range(dimension)]

    while True:
        
        # Инициализируем текущий вектор невязки 
        current_approx = [0 for _ in range(dimension)]

        # Для каждой переменной найдем ее значение на текущей итерации
        for var in range(dimension):
            
            # В соответствии с формулой инициализируем значение переменной на текущей итерации уже известными нам значениями
            current_approx[var] = matrix[var][dimension] * PARAMETER / matrix[var][var]

            # Находим недостающую часть суммы для нашей переменной, тоже в соответствии с формулой
            for other in range(dimension):
                if other < var:
                    current_approx[var] -= matrix[var][other] * current_approx[other] * PARAMETER / matrix[var][var]
                if other > var:
                    current_approx[var] -= matrix[var][other] * previous_approx[other] * PARAMETER / matrix[var][var]
    
            # Согласно формуле вычитаем из текущего значения переменной предыдущее значение переменной
            current_approx[var] -= (PARAMETER - 1) * previous_approx[var]

        for var in range(dimension - 1):
            result += f'x{var} = {previous_approx[var]}, '
        result += f'x{dimension - 1} = {previous_approx[dimension - 1]} \n'
            
        # Если вектора невязки поэлементно отличаются не более чем на допустимое значение, то прекращаем производить итерации
        if compare_arrays_equality(current_approx, previous_approx, EPS):
            result += 'Ответ: \n'
            for var in range(dimension - 1):
                result += f'x{var} = {previous_approx[var]}, '
            result += f'x{dimension - 1} = {previous_approx[dimension - 1]}'
            return result

        # Если выход из функции не произошёл, то присваиваем текущий вектор невязки предыдущему
        previous_approx = current_approx


def compare_arrays_equality(first: list, second: list, approximation: float):
    '''Функция поэлементного сравнения двух массивов в соответствии с допустимой нормой отклонения'''
    for iter in range(len(first)):
        if abs(first[iter] - second[iter]) > approximation:
            return False
    return True
