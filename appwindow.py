from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mb

from tableinput import SimpleTableInput
from solver import solve_gauss
from matrix import validate_matrix, read_from_file


class GaussWindow:
    def __init__(self):

        # Задаем параметры для главного окна
        self.root_window = Tk()
        self.root_window.iconbitmap(default='gauss.ico')
        self.root_window.title('SLAE solver')
        self.root_window.resizable(False, False)

        '''Создаём и располагаем виджеты на окне'''

        # Размещаем надпись размерности
        dimension_label = ttk.Label(text='Dimension: ')
        dimension_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        # Создаём поле ввода размерности и настраиваем валидацию
        self.current_dimension = StringVar(value='3')
        validate_cmd = self.root_window.register(self.validate_dimension)
        self.dimension_entry = ttk.Spinbox(
            self.root_window,
            from_=2,
            to=6,
            textvariable=self.current_dimension,
            validate='key',
            validatecommand=(validate_cmd, '%P'),
            wrap=True
        )
        self.current_dimension.trace('w', self.on_dimension_entry_change)
        self.dimension_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # Создаем заголовок метода
        method_label = ttk.Label(self.root_window, text='Method: ')
        method_label.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        # Создаем поле ввода метода
        self.methods = ['Метод Гаусса', 'Метод релаксации']
        self.current_method = StringVar(value=self.methods[0])
        self.method_combobox = ttk.Combobox(
            self.root_window,
            values=self.methods,
            textvariable=self.current_method,
            state='readonly'
        )
        self.method_combobox.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )

        # Обозначаем поле вывода ошибок (будет выводиться при возникновении)
        self.error_label = ttk.Label(self.root_window, foreground='#FF0000')

        # Создаем фрейм матрицы
        self.current_matrix_grid = SimpleTableInput(
            self.root_window,
            int(self.current_dimension.get()),
            int(self.current_dimension.get()) + 1
        )
        self.current_matrix_grid.grid(
            row=1,
            columnspan=4,
            padx=10,
            pady=10
        )

        # Создаем кнопку, которая будет запускать решение
        self.solve_button = ttk.Button(self.root_window, text='Solve', command=self.on_button_click)
        self.solve_button.grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )

        self.load_button = ttk.Button(self.root_window, text='Load from file', command=self.on_load)
        self.load_button.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )

        # Запускаем окно
        self.root_window.mainloop()

    # Функция, которая будет перерисовывать матрицу при изменении размерности
    def on_dimension_entry_change(self, *args):
        self.current_dimension.set(self.dimension_entry.get())
        self.current_matrix_grid.destroy()
        if self.current_dimension.get() != '':
            self.current_matrix_grid = SimpleTableInput(
                self.root_window,
                int(self.current_dimension.get()),
                int(self.current_dimension.get()) + 1)
            self.current_matrix_grid.grid(
                row=1,
                columnspan=4,
                padx=10,
                pady=10
            )

    # Функция, которая проверяет введенное значение размерности и выводит ошибки
    def validate_dimension(self, p):
        if str.isdigit(p) and int(p) in range(2, 7):
            return True
        elif p == '':
            self.error_label['text'] = 'Не введена размерность матрицы!'
            self.error_label.grid(
                row=1,
                columnspan=4,
                padx=10,
                pady=10
            )
            return True
        return False

    def on_load(self):
        ftypes = [('Текстовый документ', '*.txt')]
        dlg = filedialog.Open(self.root_window, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':
            print(fl)
            matrix = read_from_file(fl)
            print(matrix)
            if not validate_matrix(matrix, int(self.current_dimension.get())):
                mb.showerror('Ошибка', 'Матрица в файле задана некорректно!')
                return
            self.current_matrix_grid.set(matrix)
            return

    def on_button_click(self):
        answer = solve_gauss(self.current_matrix_grid.get())
        mb.showinfo('Решение', answer)
