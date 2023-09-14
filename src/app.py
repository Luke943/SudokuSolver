import os
import random
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from sudoku_solver import Grid, Sudoku


puzzles_filename = "puzzles.txt"
icon_filename = "sudoku.svg"

box_size = 40


class SudokuSolverGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.setWindowIcon(QtGui.QIcon(icon_filename))
        self.setGeometry(600, 300, box_size * 9, box_size * 10)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid = Grid()  # Initialize an empty Sudoku grid
        self.input_boxes: dict[tuple[int, int], QtWidgets.QLineEdit] = {}

        for row in range(9):
            for col in range(9):
                input_box = QtWidgets.QLineEdit()
                input_box.setMaxLength(1)
                input_box.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[1-9]*")))
                input_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                input_box.setFixedHeight(box_size)
                input_box.setFixedWidth(box_size)
                box_row = row // 3
                box_col = col // 3
                if box_row % 2 == box_col % 2:
                    input_box.setStyleSheet("background-color: powderblue")
                else:
                    input_box.setStyleSheet("background-color: moccasin")
                self.input_boxes[row, col] = input_box
                self.grid_layout.addWidget(input_box, row, col)

        load_button = QtWidgets.QPushButton("Load\npuzzle")
        load_button.clicked.connect(self.load_puzzle)
        load_button.setFixedSize(box_size * 3, box_size * 2)
        self.grid_layout.addWidget(load_button, 10, 0, 2, 3)

        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(self.clear_values)
        clear_button.setFixedSize(box_size * 3, box_size * 2)
        self.grid_layout.addWidget(clear_button, 10, 3, 2, 3)

        solve_button = QtWidgets.QPushButton("Solve")
        solve_button.clicked.connect(self.solve_sudoku)
        solve_button.setFixedSize(box_size * 3, box_size * 2)
        self.grid_layout.addWidget(solve_button, 10, 6, 2, 3)

        self.setLayout(self.grid_layout)

        # Apply stylesheet
        with open("styles.qss", "r") as fp:
            self.loadedstylesheet = fp.read()
        self.setStyleSheet(self.loadedstylesheet)

    def load_puzzle(self):
        n = random.randint(1, 50)
        start_line = n * 10 - 9
        with open(puzzles_filename, "r") as fp:
            lines = fp.readlines()[start_line : start_line + 10]
        for row in range(9):
            for col in range(9):
                ch = lines[row][col]
                if ch == "0":
                    self.input_boxes[row, col].setText("")
                    self.input_boxes[row, col].setReadOnly(False)
                else:
                    self.input_boxes[row, col].setText(lines[row][col])
                    self.input_boxes[row, col].setReadOnly(True)
        self.setStyleSheet(self.loadedstylesheet)

    def clear_values(self):
        for row in range(9):
            for col in range(9):
                self.input_boxes[row, col].setText("")
                self.input_boxes[row, col].setReadOnly(False)
        self.setStyleSheet(self.loadedstylesheet)

    def solve_sudoku(self):
        # Update the grid with the user's input
        for row in range(9):
            for col in range(9):
                text = self.input_boxes[row, col].text()
                if text.isdigit():
                    self.grid[row, col] = int(text)
                else:
                    self.grid[row, col] = 0

        # Solve the Sudoku puzzle
        sudoku = Sudoku(self.grid)
        sudoku.solve()

        if sudoku.solve_successful:
            # Update the GUI with the solved puzzle
            for row in range(9):
                for col in range(9):
                    self.input_boxes[row, col].setText(str(sudoku.grid[row, col]))
            QtWidgets.QMessageBox.information(
                self, "Sudoku Solved", "Sudoku puzzle has been solved!"
            )
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Sudoku Unsolved",
                "The Sudoku puzzle could not be solved. Check your input!",
            )


if __name__ == "__main__":
    os.chdir(sys.path[0])
    app = QtWidgets.QApplication(sys.argv)
    window = SudokuSolverGUI()
    window.show()
    sys.exit(app.exec_())
