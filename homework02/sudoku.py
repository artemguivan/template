import pathlib
import typing as tp
import random

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    group_elems = []
    answer = []
    for i, elem in enumerate(values): 
        group_elems.append(elem)
        if (((i+1) % n) == 0) :
            answer.append(group_elems)
            group_elems = []
    return answer


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """
    Return row (first element of tuple) 
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    """
    ind = pos[0]
    return grid[ind]

def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """
    Return column (second element of tuple) 
    >>> get_col([['5', '3', '.', '.', '7', '.', '.', '.', '.'],
                ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
                ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
                ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
                ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
                ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
                ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
                ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
                ['.', '.', '.', '.', '8', '.', '.', '7', '9']], (2, 0))

    ['5', '6', '.', '8', '4', '7', '.', '.', '.']
    >>> get_col([['5', '3', '.', '.', '7', '.', '.', '.', '.'],
                ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
                ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
                ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
                ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
                ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
                ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
                ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
                ['.', '.', '.', '.', '8', '.', '.', '7', '9']], (2, 0))
    
    ['3', '.', '9', '.', '.', '.', '6', '.', '.']
    """
    ind = pos[1] # стоит ли создавать новую переменную для читаемости кода?
    return [elem[pos[1]] for elem in grid]

def get_block_coord(pos: tp.Tuple[int, int]) -> tp.Tuple[int, int]: 
    """
    return start coordinates of block ()
    
    >>> get_block+coord(pos=(4, 3))
    (3, 3)
    """
    row, col = pos
    col_coord = -1
    row_coord = -1

    zones = {"012":0, 
            "345":3,
            "678":6}
    for key in zones.keys():
        if str(row) in key:
            row_coord = zones[key]

        if str(col) in key:
            col_coord = zones[key]
    return (row_coord, col_coord)

def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int], block_size=3) -> tp.List[str]:
    """
    return block of the grid
    
    >>> get_block(
        grid=[['5', '3', '.', '.', '7', '.', '.', '.', '.'],
        ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
        ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
        ['8', '.', '.', |'.', '6', '.'|, '.', '.', '3'],
        ['4', '.', '.', |'8', '.', '3'|, '.', '.', '1'],
        ['7', '.', '.', |'.', '2', '.'|, '.', '.', '6'],
        ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
        ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
        ['.', '.', '.', '.', '8', '.', '.', '7', '9']],
        pos=(4, 3))
    ['.', '6', '.', '8', '.', '3', '.', '2', '.']
    """  
    row_coord, col_coord = get_block_coord(pos)

    block_values = []
    for r in range(row_coord, row_coord + block_size):
        for c in range(col_coord, col_coord + block_size):
            block_values.append(grid[r][c])
    
    return block_values


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """
    Find the first empty space on the grid
    return row, column

    >>> find_empty_positions(['.', '6', '.', '8', '.', '3', '.', '2', '.'])
    (0, 0)

    >>> find_empty_positions(
        grid=[['5', '3', '.', '.', '7', '.', '.', '.', '.'],
            ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
            ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
            ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
            ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
            ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
            ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
            ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
            ['.', '.', '.', '.', '8', '.', '.', '7', '9']])
    (0, 2)
    """

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == ".":
                return (row, col)
    return None
            

def find_possible_values(grid: tp.List[tp.List[str]], empty_col: int, empty_row: int):
    """ 
    return possible values for filling the sudoku
    >>> get_possible_values(
    grid = [['5', '3', '.', '.', '7', '.', '.', '.', '.'],
            ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
            ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
            ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
            ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
            ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
            ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
            ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
            ['.', '.', '.', '.', '8', '.', '.', '7', '9']],
        empty_col=2, empty_row=0)
    {'1', '2', '4', '6', '9'}
    """

    possible_values = set(str(x) for x in range(1, len(grid[0])+1))
    unpossible_values = (
        set(get_row(grid, (empty_row, empty_col))) |
        set(get_col(grid, (empty_row, empty_col))) |
        set(get_block(grid, (empty_row, empty_col)))
    )

    return possible_values - unpossible_values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """
    Solution.
    """
    empty_pos = find_empty_positions(grid)
    if not empty_pos:
        return grid

    empty_row, empty_col = empty_pos
    possible_values = find_possible_values(grid=grid, empty_row=empty_row, empty_col=empty_col)
    
    for value in possible_values:
        grid[empty_row][empty_col] = value
        if solve(grid):
            return grid
        grid[empty_row][empty_col] = '.'
    return None


def check_solution(solution):
    """
    return answer on your question

    """
    cols = [len(set(get_col(solution, pos=(0, i)))) for i in range(9)]
    rows = [len(set(get_row(solution, pos=(i, 0)))) for i in range(9)]
    blocks = [len(set(get_block(grid, pos=(i, j)))) for i in range(2, 9, 3) for j in range(2, 9, 3)]
    return (cols == rows == blocks)


def generate_full_sudoku() -> tp.List[tp.List[str]]:
    """Generate all sudoku"""
    grid = [["." for _ in range(9)] for _ in range(9)]
    solve(grid) 
    return grid


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = generate_full_sudoku()
    
    filled_positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(filled_positions)
    to_remove = max(0, 81 - N)

    for i, j in filled_positions[:to_remove]:
        grid[i][j] = "."

    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)



