from calendar import c
from tkinter import Tk, ttk, filedialog, messagebox as mb, StringVar

from window_components.slaeinput import SimpleSlaeInput
from logic.gauss import solve_gauss
from logic.relax import solve_relaxation
from logic.matrix import validate_matrix, read_from_file


class GaussWindow(Tk):
    def __init__(self):

        # Задаем параметры для главного окна
        super().__init__()
        self.title('SLAE solver')
        self.resizable(False, False)

        # Создаём и размещаем компоненты на окне 
        self.init_window()

        # Запускаем приложение
        self.mainloop()

    # Функция создаёт и размещает виджеты на окне
    def init_window(self):

        # Надпись "Dimension"
        dimension_label = ttk.Label(text='Dimension: ')
        dimension_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        # Поле ввода размерности
        self.current_dimension = StringVar(value='3')
        validate_cmd = self.register(self.validate_dimension)
        self.dimension_entry = ttk.Spinbox(
            self,
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
        method_label = ttk.Label(self, text='Method: ')
        method_label.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        # Создаем поле ввода метода
        self.methods = ['Метод Гаусса', 'Метод релаксации']
        self.current_method = StringVar(value=self.methods[0])
        self.solver = solve_gauss
        self.method_combobox = ttk.Combobox(
            self,
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
        self.method_combobox.bind('<<ComboboxSelected>>', self.on_change_method)

        # Обозначаем поле вывода ошибок (будет выводиться при возникновении)
        self.error_label = ttk.Label(self, foreground='#FF0000')

        # Создаем фрейм матрицы
        self.current_matrix_grid = SimpleSlaeInput(
            self,
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
        self.solve_button = ttk.Button(self, text='Solve', command=self.on_solve_click)
        self.solve_button.grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )

        self.load_button = ttk.Button(self, text='Load from file', command=self.on_load_click)
        self.load_button.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )

    # Функция изменения фрейма матрицы при изменении размерности пользователем
    def on_dimension_entry_change(self, *args):
        self.current_dimension.set(self.dimension_entry.get())
        self.current_matrix_grid.destroy()
        if self.current_dimension.get() != '':
            self.current_matrix_grid = SimpleSlaeInput(
                self,
                int(self.current_dimension.get()),
                int(self.current_dimension.get()) + 1)
            self.current_matrix_grid.grid(
                row=1,
                columnspan=4,
                padx=10,
                pady=10
            )

    # Функция осуществляет валидацию введенной размерности 
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

    # Функция вызывается при нажатии на кнопку загрузки матрицы
    def on_load_click(self):
        ftypes = [('Текстовый документ', '*.txt')]
        dlg = filedialog.Open(self, filetypes=ftypes)
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

    # Функция вызывается при нажатии на кнопку решения системы
    def on_solve_click(self):
        if self.current_matrix_grid.check_full_matrix_input():
            answer = self.solver(self.current_matrix_grid.get())
            mb.showinfo('Решение', answer)
        else: 
            mb.showerror('Ошибка', 'Матрица введена не полностью')

    def on_change_method(self, event):
        if self.current_method.get() == self.methods[0]:
            self.solver = solve_gauss
            return
        if self.current_method.get() == self.methods[1]:
            self.solver = solve_relaxation
            return
        self.solver = solve_gauss
        return
