EPS = 0.00000000001

def solve_gauss(matrix: list):
    rows: int = len(matrix)
    columns: int = len(matrix[0]) - 1

    # Заполняем массив, который для каждого столбца будет содержать строку опорного элемента, или -1 если его нет
    where: list = [False for _ in range(columns)]
    for col in range(columns):

        # Выбираем главную строку по максимальному элементу столбца
        pivot: int = col
        for lower_row in range(col, rows):
            if abs(matrix[lower_row][col]) > abs(matrix[pivot][col]): 
                pivot = lower_row
            
        # Проверяем является ли наш опорный элемент 0 или близким к 0 
        if abs(matrix[pivot][col]) < EPS:
            continue

        # Если наш опорный элемент таковым не оказался, то поднимаем строку вверх
        for right_column in range(columns + 1):
            matrix[pivot][right_column], matrix[col][right_column] = matrix[col][right_column], matrix[pivot][right_column]
            where[col] = True

        # Далее зануляем всю нижнюю часть столбца
        for row in range(rows):
            if row != col:
                factor: float = matrix[row][col] / matrix[col][col]
                for right_column in range(col, columns + 1):
                    matrix[row][right_column] -= matrix[col][right_column] * factor

    # Проверяем имеет ли система бесконечное количество решений
    for col in range(columns):
        if not where[col]:
            return 'Система имеет бесконечное количество решений'
    
    # Выясняем решения системы
    answer: list = [0 for _ in range(columns)]
    
    # Для каждой переменной пытаемся найти ответ
    for col in range(columns):
        answer[col] = matrix[col][columns] / matrix[col][col]

    # Проверяем есть ли решения у системы
    for row in range(rows):

        # Ищем сумму корней умноженных на коэффиценты
        sum: float = 0
        for col in range(columns):
            sum += answer[col] * matrix[row][col]

        # Сравниваем их со свободным членом. Если разница достаточно велика, то решений у системы нет
        if abs(sum - matrix[row][columns]) > EPS:
            return 'Система не имеет решений'
    
    # Если система имеет ровно 1 решение, то выводим его
    result: str = ''
    for item in range(len(answer)):
        result += f'x{item + 1} = {answer[item]}, '
    return result