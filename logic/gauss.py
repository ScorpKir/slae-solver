def check_matrix_consistent(matrix: list):
    return True

def solve_gauss(matrix: list):
    '''Функция решает СЛАУ (заданную в виде матрицы) методом Гаусса'''
    # Результат, который мы будем выводить
    result: str = 'Матрица после приведения к ступенчатому виду: \n'

    # Обозначаем допустимую погрешность
    EPS = 0.0001

    # Получаем размерность матрицы
    dimension = len(matrix)

    # Заполняем массив, который для каждого столбца будет содержать строку опорного элемента, или -1 если его нет
    where: list = [False for _ in range(dimension)]
    for col in range(dimension):

        # Выбираем главную строку по максимальному элементу столбца
        pivot: int = col
        for lower_row in range(col, dimension):
            if abs(matrix[lower_row][col]) > abs(matrix[pivot][col]): 
                pivot = lower_row
            
        # Проверяем является ли наш опорный элемент 0 или близким к 0 
        if abs(matrix[pivot][col]) < EPS:
            continue

        # Если наш опорный элемент таковым не оказался, то поднимаем строку вверх
        for right_column in range(dimension + 1):
            matrix[pivot][right_column], matrix[col][right_column] = matrix[col][right_column], matrix[pivot][right_column]
            where[col] = True

        # Далее зануляем всю нижнюю часть столбца
        for row in range(dimension):
            if row != col:
                factor: float = matrix[row][col] / matrix[col][col]
                for right_column in range(col, dimension + 1):
                    matrix[row][right_column] -= matrix[col][right_column] * factor

    # Проверяем имеет ли система бесконечное количество решений
    for col in range(dimension):
        if not where[col]:
            return 'Система имеет бесконечное количество решений'
    
    # Выясняем решения системы
    answer: list = [0 for _ in range(dimension)]
    
    # Для каждой переменной пытаемся найти ответ
    for col in range(dimension):
        answer[col] = matrix[col][dimension] / matrix[col][col]

    # Проверяем есть ли решения у системы
    for row in range(dimension):

        # Ищем сумму корней умноженных на коэффиценты
        sum: float = 0
        for col in range(dimension):
            sum += answer[col] * matrix[row][col]

        # Сравниваем их со свободным членом. Если разница достаточно велика, то решений у системы нет
        if abs(sum - matrix[row][dimension]) > EPS:
            return 'Система не имеет решений'

    for row in matrix:
        [result.join(str(elem) + ' ') for elem in row] + '\n'

    # Если система имеет ровно 1 решение, то выводим его
    result += 'Решение системы уравнений: \n'
    for item in range(len(answer) - 1):
        result += f'x{item + 1} = {answer[item]}, '
    result += f'x{len(answer)} = {answer[len(answer) - 1]}'
    return result