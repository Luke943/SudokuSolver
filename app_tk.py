from itertools import product
import tkinter as tk

import sudoku

root = tk.Tk()
root.title("Sudoku Solver")
root.geometry("324x440")

label = tk.Label(root, text="Fill in the numbers and click solve")
label.grid(row=0, column=1, columnspan=10)
error_label = tk.Label(root, text="", foreground="red")
error_label.grid(row=15, column=1, columnspan=10, pady=5)
solved_label = tk.Label(root, text="", foreground="green")
solved_label.grid(row=15, column=1, columnspan=10, pady=5)

cells = {}


def valid_input(entry: str) -> bool:
    return (entry.isdigit() and len(entry) == 1 and entry != "0") or entry == ""


reg = root.register(valid_input)


def draw_3x3_grid(row: int, column: int, bgcolour: str) -> None:
    for i, j in product(range(3), range(3)):
        e = tk.Entry(
            root,
            width=5,
            bg=bgcolour,
            justify=tk.CENTER,
            validate="key",
            validatecommand=(reg, "%P"),
        )
        e.grid(
            row=row + i + 1,
            column=column + j + 1,
            sticky="nsew",
            padx=1,
            pady=1,
            ipady=5,
        )
        cells[row + i + 1, column + j + 1] = e


def draw_9x9_grid() -> None:
    colour = "#D0ffff"
    for row, column in product(range(1, 10, 3), range(0, 9, 3)):
        draw_3x3_grid(row, column, colour)
        if colour == "#D0ffff":
            colour = "#ffffd0"
        else:
            colour = "#D0ffff"


def clear_values() -> None:
    error_label.configure(text="")
    solved_label.configure(text="")
    for row, column in product(range(2, 11), range(1, 10)):
        cell = cells[row, column]
        cell.delete(0, "end")


def get_values() -> sudoku.Grid:
    error_label.configure(text="")
    solved_label.configure(text="")
    grid = sudoku.Grid()
    for row, column in product(range(2, 11), range(1, 10)):
        value = cells[row, column].get()
        grid[row - 2, column - 1] = value if value else 0
    return grid


solve_btn = tk.Button(root, text="Solve", command=get_values, width=10)
solve_btn.grid(row=20, column=1, columnspan=5, pady=20)

clear_btn = tk.Button(root, text="Clear", command=clear_values, width=10)
clear_btn.grid(row=20, column=5, columnspan=5, pady=20)

draw_9x9_grid()
root.mainloop()
