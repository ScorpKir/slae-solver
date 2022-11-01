from tkinter import END, ttk

class SimpleSlaeInput(ttk.Frame):
    '''Класс фрейма ввода системы уравнений'''
    def __init__(self, parent, rows, columns):
        super().__init__(parent)

        self._entry = {}
        self.rows = rows
        self.columns = (columns - 1) * 2 + 1

        # Создаем саму таблицу
        self._create_entry()

        # Устанавливаем одинаковое масштабироание для всех элементов
        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)
        self.grid_rowconfigure(self.rows, weight=1)


    # Для каждой строки чередуем надписи и поля для ввода
    def _create_entry(self):
        vcmd = (self.register(self._validate), "%P")
        for row in range(self.rows):
            var_index = 1
            for column in range(self.columns):
                index = (row, column)
                if column % 2 == 0:
                    e = ttk.Entry(self, validate="key", validatecommand=vcmd)
                    e.grid(row=row, column=column, stick="nsew")
                    self._entry[index] = e
                else:
                    text = f'x{var_index} + ' if column != self.columns - 2 else f'x{var_index} = '
                    e = ttk.Label(self, text=text)
                    e.grid(row=row, column=column)
                    self._entry[index] = e
                    var_index += 1


    def get(self):
        result = []
        for row in range(self.rows):
            current_row = []
            for column in range(0, self.columns, 2):
                index = (row, column)
                current_row.append(float(self._entry[index].get()))
            result.append(current_row)
        return result
    

    def set(self, matrix):
        for row in range(self.rows):
            for column in range(0, self.columns + 1, 2):
                index = (row, column)
                self._entry[index].delete(0, END)
                self._entry[index].insert(0, str(matrix[row][column // 2]))


    def _validate(self, P):
        '''Функция проверяет значение, вводимое в поле ввода'''
        if P.strip() == '' or P.strip() == '-' or P.strip() == '.':
            return True
        try:
            f = float(P)
        except ValueError:
            self.bell()
            return False
        return True


    def check_full_matrix_input(self):
        '''Функция, которая осуществляет проверку полного ввода матрицы'''
        for row in range(self.rows):
            for column in range(0, self.columns, 2):
                index = (row, column)
                if self._entry[index].get() == '':
                    return False
        return True
