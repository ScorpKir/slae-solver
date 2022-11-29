import numpy as np
from tkinter import Tk, ttk, filedialog, messagebox as mb, StringVar

from window_components.slaeinput import SimpleSlaeInput
from window_components.sor_log_window import AnswerWindow
from logic.gauss import gauss
from logic.sor import sor


class GaussWindow(Tk):
    def __init__(self):

        # Параметры для главного окна
        super().__init__()
        self.title('SLAE solver')
        self.resizable(False, False)

        # Надпись "Dimension"
        dimension_label: ttk.Label = ttk.Label(text='Dimension: ')
        dimension_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        # Поле ввода размерности
        self.current_dimension: StringVar = StringVar(value='3')
        validate_cmd: callable = self.register(self.validate_dimension)
        self.dimension_entry: ttk.Spinbox = ttk.Spinbox(
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

        # Заголовок метода
        method_label: ttk.Label = ttk.Label(self, text='Method: ')
        method_label.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        # Поле выбора метода
        self.methods: list = ['Метод Гаусса', 'Метод релаксации']
        self.current_method: StringVar = StringVar(value=self.methods[0])
        self.solver: callable = gauss
        self.method_combobox: ttk.Combobox = ttk.Combobox(
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

        # Поле вывода ошибок (будет выводиться при возникновении)
        self.error_label: ttk.Label = ttk.Label(self, foreground='#FF0000')

        # Фрейм матрицы
        self.current_matrix_grid: SimpleSlaeInput = SimpleSlaeInput(
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

        # Кнопка запуска решения
        self.solve_button: ttk.Button = ttk.Button(self, text='Solve', command=self.on_solve_click)
        self.solve_button.grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )

        # Кнопка загрузки матрицы из файла
        self.load_button: ttk.Button = ttk.Button(self, text='Load from file', command=self.on_load_click)
        self.load_button.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )

        # Запускаем приложение
        self.mainloop()

    def on_dimension_entry_change(self, *args):
        '''
        Триггер динамически изменяет фрейм матрицы при изменении размерности СЛАУ пользователем
        '''

        # Изменяем текущую размерность
        self.current_dimension.set(self.dimension_entry.get())

        # Удаляем старый фрейм матрицы
        self.current_matrix_grid.destroy()

        # Если размерность не пустая, то пересоздаем фрейм
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
 
    def validate_dimension(self, p) -> bool:
        '''
        Функция валидации значения, введенного в поле размерности
        Принимает введенное значение
        Возвращает True, если значение корректно, иначе возвращает False
        '''

        # Если введенное значение - целое число в диопазоне от 2 до 7, то возвращаем True
        if str.isdigit(p) and int(p) in range(2, 7):
            return True

        # Если значение не введено, то выводим сообщение о том, что размерность матрицы не введена
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

    def on_load_click(self) -> None:
        '''
        Триггер запускает диалоговое окно для выбора файла и считывания из него матрицы
        '''
        
        # Допустимые типы файлов
        ftypes: list = [('Текстовый документ', '*.txt')]

        # Открываем диалоговое окно
        dlg = filedialog.Open(self, filetypes=ftypes)
        fl = dlg.show()

        # Если файл был выбран, то загружаем матрицу из файла
        if fl != '':
            self.current_matrix_grid.set(np.loadtxt(fl, dtype=float))

    def on_solve_click(self):
        '''
        Триггер запускает решение системы введенной системы линейных алгебраических уравнений
        '''

        # Если матрица введена полностью, то вычисляем решение и выводим его пользователю
        if self.current_matrix_grid.check_full_matrix_input():
            answer = self.solver(np.array(self.current_matrix_grid.get(), dtype=float))
            AnswerWindow(self, answer)
        # Иначе выводим ошибку о том, что матрицы не введена полностью
        else: 
            mb.showerror('Ошибка', 'Матрица введена не полностью')

    def on_change_method(self, event):
        '''
        Триггер меняет функцию, находяющую решение СЛАУ в зависимости от выбранного метода
        '''

        # Если выбранный метод - метод Гаусса, то выбираем его
        if self.current_method.get() == self.methods[0]:
            self.solver = gauss
            return

        # Если выбранный метод - метод релаксации, то выбираем его
        if self.current_method.get() == self.methods[1]:
            self.solver = sor
            return

        # Если ни один из методов не выбран, то используем метод гаусса
        self.solver = gauss
