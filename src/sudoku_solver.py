from collections import Counter

EMPTY_GRID = [[0 for _ in range(9)] for _ in range(9)]


class Grid:
    """Grid to hold values of a sudoku puzzle."""

    def __init__(self, values: list[list[int]] = EMPTY_GRID):
        self._values = values

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self._values[key[1]][key[0]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        self._values[key[1]][key[0]] = value

    def __str__(self) -> str:
        grid_string = "\n"
        for j in range(9):
            for i in range(9):
                grid_string += str(self[i, j]) + " "
                if i == 2 or i == 5:
                    grid_string += "| "
                elif i == 8:
                    grid_string += "\n"
            if j == 2 or j == 5:
                grid_string += "-" * 6 + "+" + "-" * 7 + "+" + "-" * 6 + "\n"
        return grid_string


class Sudoku:
    """Sudoku solver class."""

    def __init__(self, grid: Grid = Grid()):
        self.grid = grid
        self.solve_attempted = False
        self.solve_successful = False

    def solve(self) -> None:
        self.solve_attempted = True
        if not self.is_valid_grid():
            self.solve_successful = False
            return
        self._solve()
        self.solve_successful = all(self.grid[i, j] for i in range(9) for j in range(9))

    def _solve(self) -> bool:
        for row, column in (
            (i, j) for i in range(9) for j in range(9) if self.grid[(i, j)] == 0
        ):
            for value in range(1, 10):
                if self._is_valid_input((row, column), value):
                    self.grid[row, column] = value
                    if self._solve():
                        return True
                    self.grid[row, column] = 0
            return False  # No values work
        return True  # Solution found

    def _is_valid_input(self, position: tuple[int, int], value: int) -> bool:
        row, column = position
        if value in (self.grid[row, j] for j in range(9)):
            return False
        if value in (self.grid[i, column] for i in range(9)):
            return False
        box_row = (row // 3) * 3
        box_column = (column // 3) * 3
        if value in (
            self.grid[i, j]
            for i in range(box_row, box_row + 3)
            for j in range(box_column, box_column + 3)
        ):
            return False
        return True

    def is_valid_grid(self) -> bool:
        for row in range(9):
            counter = Counter(self.grid[row, j] for j in range(9) if self.grid[row, j])
            if counter:
                if max(counter.values()) > 1:
                    return False
        for col in range(9):
            counter = Counter(self.grid[i, col] for i in range(9) if self.grid[i, col])
            if counter:
                if max(counter.values()) > 1:
                    return False
        for row, col in ((3 * i, 3 * j) for i in range(3) for j in range(3)):
            counter = Counter(
                self.grid[row + i, col + j]
                for i in range(3)
                for j in range(3)
                if self.grid[row + i, col + j]
            )
            if counter:
                if max(counter.values()) > 1:
                    return False
        return True

    def __str__(self) -> str:
        return str(self.grid)


if __name__ == "__main__":
    test_grid = Grid(
        [
            [0, 0, 3, 0, 2, 0, 6, 0, 0],
            [9, 0, 0, 3, 0, 5, 0, 0, 1],
            [0, 0, 1, 8, 0, 6, 4, 0, 0],
            [0, 0, 8, 1, 0, 2, 9, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 0, 6, 7, 0, 8, 2, 0, 0],
            [0, 0, 2, 6, 0, 9, 5, 0, 0],
            [8, 0, 0, 2, 0, 3, 0, 0, 9],
            [0, 0, 5, 0, 1, 0, 3, 0, 0],
        ]
    )
    sudoku = Sudoku(test_grid)
    print(sudoku)
    sudoku.solve()
    print(sudoku)
    print(sudoku.solve_attempted)
    print(sudoku.solve_successful)
