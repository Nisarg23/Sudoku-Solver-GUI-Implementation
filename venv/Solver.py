import math


def vertical_check(s):
    for i in range(9):
        r = []
        r.append(s[i])
        r.append(s[i + 9])
        r.append(s[i + 18])
        r.append(s[i + 27])
        r.append(s[i + 36])
        r.append(s[i + 45])
        r.append(s[i + 54])
        r.append(s[i + 63])
        r.append(s[i + 72])

        for a in range(len(r)):
            for b in range(a + 1, len(r), 1):
                if r[a] == r[b] and r[a] is not None:
                    return i + 1

    return None


def horizontal_check(s):
    row = None
    for i in range(0, 81, 9):
        r = []
        r.append(s[i])
        r.append(s[i + 1])
        r.append(s[i + 2])
        r.append(s[i + 3])
        r.append(s[i + 4])
        r.append(s[i + 5])
        r.append(s[i + 6])
        r.append(s[i + 7])
        r.append(s[i + 8])

        for a in range(len(r)):
            for b in range(a + 1, len(r), 1):
                if r[a] == r[b] and r[a] is not None:
                    return (i+9)//9

    return None


def box_check(s):
    box = None
    for j in range(0, 7, 3):
        for i in range(j * 9, j * 9 + 7, 3):
            r = []
            r.append(s[i])
            r.append(s[i + 1])
            r.append(s[i + 2])
            r.append(s[i + 9])
            r.append(s[i + 10])
            r.append(s[i + 11])
            r.append(s[i + 18])
            r.append(s[i + 19])
            r.append(s[i + 20])

            for a in range(len(r)):
                for b in range(a + 1, len(r), 1):
                    if r[a] == r[b] and r[a] is not None:
                        if j == 0:
                            if i == 0:
                                box = 1
                            elif i == 3:
                                box = 2
                            elif i == 6:
                                box = 3
                        elif j == 3:
                            if i == 27:
                                box = 4
                            elif i == 30:
                                box = 5
                            elif i == 33:
                                box = 6
                        elif j == 6:
                            if i == 54:
                                box = 7
                            elif i == 57:
                                box = 8
                            elif i == 60:
                                box = 9
                        else:
                            box = ((i / 3 / 9) + 1)
                        return box

    return None

def find_empty(board):
    for i in range (9):
        for j in range (9):
            if board[i * 9 + j] is None:
                return i * 9 + j

    return None

def valid(board):
    if box_check(board) is None and vertical_check(board) is None and horizontal_check(board) is None:
        return True
    return False

def solve(board):
    index = find_empty(board)

    if not index:
        return True

    for i in range(1,10):
        board[index] = i
        if valid(board):
            if solve(board):
                return True

        board[index] = None

    return False


# prints sudoku template puzzle
def print_board():
    for i in range(9):
        if i % 3 == 0 and i!= 0:
            print("")
        for j in range(9):
            if not_solved[i * 9 + j] is None:
                if j % 3 == 0 and j!=0:
                    print("  |_ _|", end="")
                else:
                    print("|_ _|", end="")
            else:
                if j % 3 == 0 and j != 0:
                    print("  |_" + str(not_solved[i * 9 + j]) + "_|", end="")
                else:
                    print("|_" + str(not_solved[i * 9 + j]) + "_|", end="")
        print("")


not_solved = [7, 8, None, 4, None, None, 1, 2, None,
              6, None, None, None, 7, 5, None, None, 9,
              None, None, None, 6, None, 1, None, 7, 8,
              None, None, 7, None, 4, None, 2, 6, None,
              None, None, 1, None, 5, None, 9, 3, None,
              9, None, 4, None, 6, None, None, None, 5,
              None, 7, None, 3, None, None, None, 1, 2,
              1, 2, None, None, None, 7, 4, None, None,
              None, 4, 9, 2, None, 6, None, None, 7]
# solution to sudoku

