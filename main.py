from appwindow import GaussWindow
from tkinter import ttk

def main():
    GaussWindow()
    for theme in ttk.Style().theme_names():
        print(theme)


if __name__ == '__main__':
    main()
