import numpy as np
from tkinter import Tk, Text, Scrollbar, Toplevel, RIGHT

class AnswerWindow(Toplevel):

    def __init__(self, parent: Tk, sor_info: str):
        
        # Параметры окна
        super().__init__(parent)

        # Поле для вывода информации
        AnswerWindow.text: Text = Text(self)
        AnswerWindow.text.insert(1.0, sor_info)
        AnswerWindow.text.pack(fill='x')

        # Ползунок для движения по ответу
        AnswerWindow.scrollbar: Scrollbar = Scrollbar(self, command=self.text.yview)
        AnswerWindow.scrollbar.pack(side=RIGHT, fill='y')
        AnswerWindow.text.config(yscrollcommand=self.scrollbar.set)

        # Информация о решении
        self.stats: str = sor_info

        # Главный цикл окна
        AnswerWindow.mainloop(self)
