from tkinter import END
from tkinter import ttk


class SimpleTableInput(ttk.Frame):
    def __init__(self, parent, rows, columns):
        ttk.Frame.__init__(self, parent)

        self._entry = {}
        self.rows = rows
        self.columns = columns

        vcmd = (self.register(self._validate), "%P")

        for row in range(self.rows):
            col_index = 1
            for column in range(self.columns):
                index = (row, column)
                e = ttk.Entry(self, validate="key", validatecommand=vcmd)
                e.grid(row=row, column=column, stick="nsew")
                self._entry[index] = e
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(rows, weight=1)

    def get(self):
        result = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                index = (row, column)
                current_row.append(float(self._entry[index].get()))
            result.append(current_row)
        return result
    
    def set(self, matrix):
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column)
                self._entry[index].delete(0, END)
                self._entry[index].insert(0, str(matrix[row][column]))

    def _validate(self, P):
        if P.strip() == '' or P.strip() == '-' or P.strip() == '.':
            return True

        try:
            f = float(P)
        except ValueError:
            self.bell()
            return False
        return True
